# Hubble ↔ LiteLLM Authentication Integration — Approach

## Goal
Let anyone already logged into Hubble use the LiteLLM proxy without creating a separate LiteLLM login or API key. As stated by the lead: *"This helps everyone to login with Hubble creds, no need to setup another authentication method."*

## What we found out about Hubble's auth

| Check | Finding |
|---|---|
| Login mechanism | Direct XHR `POST` to Hubble's own `/login` endpoint — no redirect to an external identity provider |
| Token type | Hubble issues its own JWT on login |
| Token storage | Stored in browser `localStorage`, sent as `Authorization: Bearer <token>` on subsequent API calls |
| Session cookie | None — `Set-Cookie` header is absent; this is token-based auth, not cookie/session-based |
| Signing algorithm | `HS512` — a **symmetric** algorithm (same secret used to sign and verify) |
| OIDC discovery | Not applicable — Hubble is not exposing standard OIDC endpoints (`/.well-known/openid-configuration`, `/oauth2/authorize`, etc.) |

**Conclusion:** Hubble is a custom, internally-built auth system that issues its own Bearer JWTs. It is *not* an OIDC/OAuth2 provider and cannot be plugged into LiteLLM's built-in OIDC/SSO config as-is.

## Approaches considered

1. **Share Hubble's HMAC signing secret with LiteLLM** so LiteLLM can verify JWTs itself.
   - Ruled out: tightly couples two systems via a shared secret; a security liability; contradicts "no separate auth method" in spirit since it requires a security exception rather than reuse of existing infra.
2. **Ask Hubble's team to add RS256 signing + a JWKS endpoint**, turning it into a real OIDC-style provider.
   - Ruled out for now: correct long-term fix, but it's a change request to another team's system, not something we control on the LiteLLM side. Bigger ask than the stated goal requires.
3. **Token-forwarding via a custom auth handler** — LiteLLM takes the Bearer token a user already has from Hubble and forwards it to an existing Hubble API endpoint to check if it's valid, instead of verifying the signature itself. ✅ **Selected approach.**

## Selected approach: Custom Auth Handler (token forwarding)

### How it works
1. User is already logged into Hubble and holds a valid Bearer JWT (from `localStorage`).
2. That same token is sent as `Authorization: Bearer <token>` on every request to the LiteLLM proxy.
3. LiteLLM's `custom_auth` hook intercepts the request, extracts the token, and calls an existing Hubble API endpoint (whatever endpoint Hubble's own frontend already calls to fetch the logged-in user's profile) with that same Bearer token.
4. If Hubble responds `200` with user info → LiteLLM treats the request as authenticated, maps the returned fields to a LiteLLM `UserAPIKeyAuth` object (user ID, email, role, team).
5. If Hubble responds `401`/error → LiteLLM rejects the request.

No new authentication system is introduced. No secret is shared between the two systems. Hubble remains the single source of truth for who is logged in.

### Implementation sketch

```python
# hubble_auth.py
import httpx
from fastapi import Request, HTTPException
from litellm.proxy._types import UserAPIKeyAuth

async def hubble_custom_auth(request: Request, api_key: str) -> UserAPIKeyAuth:
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            "https://hubble.miraclesoft.com/api/user/me",  # placeholder — actual endpoint TBD
            headers={"Authorization": f"Bearer {api_key}"},
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid Hubble token")

    user = resp.json()
    return UserAPIKeyAuth(
        user_id=user.get("loginId"),
        user_email=user.get("email"),
        user_role="internal_user",   # can be mapped to proxy_admin for specific Hubble roles/flags
        team_id=user.get("departmentId"),
    )
```

```yaml
# config.yaml
general_settings:
  custom_auth: hubble_auth.hubble_custom_auth
```

### Trade-offs to flag
- **Latency/load**: this validation call fires on every LiteLLM request, adding one extra network hop and load on whatever Hubble endpoint we call. Worth checking that endpoint can handle the added traffic, or caching valid tokens for a short TTL (bounded by token expiry) to reduce repeat calls.
- **Token lifetime**: Hubble tokens are short-lived (~5 hours based on `iat`/`exp`). Once expired, the user needs to re-authenticate against Hubble to get a fresh token — LiteLLM has no role in refreshing it.
- **Role mapping**: Hubble's JWT carries many fine-grained access flags (department, designation, various access booleans). We'll need to decide which of these (if any) map to LiteLLM roles (`internal_user`, `team`, `proxy_admin`) versus being ignored.

## Open questions for the Hubble team

1. **Which endpoint should we call to validate a token?** Is there a lightweight "who am I" / profile endpoint that's safe and intended to be called frequently (on every LiteLLM request), or should a dedicated introspection endpoint be added instead?
2. **Rate limits / load expectations** — can that endpoint handle being hit on every LiteLLM API call, or do we need to negotiate a caching strategy on our side?
3. **Token expiry behavior** — should LiteLLM reject a request outright on an expired token, or is there a refresh mechanism on Hubble's side we should be aware of?
4. **Role/claims mapping** — which fields in the Hubble JWT (department, designation, team lead flag, admin flag, etc.) should determine a user's role/access level inside LiteLLM?
5. **Revocation** — if a user's Hubble access is revoked mid-session (offboarding, role change), does the existing token immediately become invalid at the endpoint we're calling, or does it stay "valid" until natural expiry?
6. **Environment scope** — is this endpoint the same across Hubble's environments (dev/staging/prod), and which one should LiteLLM point to in each of our environments?
7. **Ownership/support** — who do we go to if this validation call starts failing in production (which team owns uptime for the endpoint we depend on)?

## Next step
Share questions 1–7 with Hubble's backend team; once we have the validation endpoint confirmed, the `custom_auth` handler above can be finalized and tested end-to-end.
