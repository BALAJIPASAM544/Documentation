OIDC SETUP

External Requirements (Request from IT/Security Admins)
To bind LiteLLM with our corporate identity provider, We have to reach out to IT to register LiteLLM as an application and provide the standard OpenID Connect endpoints:
Redirect Callback URL (Provided to IT): https://<our-litellm-domain>/sso/callback
Awaiting from IT:
Client ID & Client Secret
Authorization Endpoint URL
Token Endpoint URL
User info Endpoint URL

Environmental Infrastructure (Configured inside LiteLLM)
Once IT returns the credentials, they will be injected directly into the LiteLLM container infrastructure as environment variables:
PROXY_BASE_URL="https://<our-litellm-domain>"
GENERIC_CLIENT_ID="<client-id>"
GENERIC_CLIENT_SECRET="<client-secret>"
GENERIC_AUTHORIZATION_ENDPOINT="<auth-url>"
GENERIC_TOKEN_ENDPOINT="<token-url>"
GENERIC_USERINFO_ENDPOINT="<userinfo-url>"
GENERIC_SCOPE="openid email profile

To finalize the setup, we should confirm two things that:
Scope of OIDC: Are we using OIDC strictly to secure Admin UI/Dashboard access for our internal team, or do you want end-user LLM API calls to be authenticated via JWT tokens?
Role Mapping: Do you want specific user groups (e.g., your core research team) to automatically map to the proxy_admin role upon their first login, or should access be granted manually?
-> Restart your LiteLLM server after adding these. When you navigate to your LiteLLM dashboard URL, you will now see a "Login with SSO" button that redirects to your corporate login page.


STEPS INVOLVED are :
Setting up OIDC is actually a very linear process.
Because OIDC requires two systems to talk to each other, the setup happens in four chronological parts. Here is the step-by-step roadmap from the absolute beginning to the final working login screen.
🗺️ The OIDC Setup Journey at a Glance
 

Part 1: Registering the Application in your Identity Provider (IdP)
Before LiteLLM can speak to your company's login system (like Okta, Microsoft Entra/Azure, Keycloak, or Authentik), you have to create a profile for it there.
Log into your IdP Management Console (or have your IT/Security admin do this).
Create a new OIDC App Integration(Choose "Web Application" as the application type).
Configure the Redirect URIs: This is the most critical setting. It tells the security provider exactly where to send the user after they successfully log in.
Sign-in Redirect URI:https://<your-litellm-domain>/sso/callback
Sign-out Redirect URI (Optional):https://<your-litellm-domain>


Part 2: Gathering the Integration Secrets
Once the application is registered in your corporate system, it will automatically generate configuration strings. Collect these five specific metrics from the IdP dashboard: 
Client ID: A unique public identifier string for LiteLLM (e.g., litellm-proxy-prod).
Client Secret: A private password that only LiteLLM and your IdP know. Keep this completely safe.
Authorization Endpoint: The web URL where users are redirected to type their username and password.
Token Endpoint: The internal API URL LiteLLM calls to exchange login authorization codes for secure user access tokens.
Userinfo Endpoint: The API endpoint LiteLLM queries to find out the logged-in user's email address and name.
💡 Quick Tip: Almost all providers publish a single public discovery link ending in .well-known/openid-configuration. If you can find that URL, it lists items 3, 4, and 5 for you automatically.



Part 3: Injecting the Credentials into LiteLLM
Now that you have the secrets, you tell LiteLLM to use them. You do this by creating or updating the environment variables where your LiteLLM application runs (your docker container, Kubernetes cluster, or local command line).
Add these variables to your environment setup:

Part 4: Testing the Implementation Loop
Save your changes and restart your LiteLLM proxy instance.
Open an incognito browser tab and navigate to the LiteLLM Admin UI domain ([https://your-litellm-proxy-domain.com/ui](https://your-litellm-proxy-domain.com/ui)).
You will be greeted with a "Login with SSO" option. Click it. 
If everything is configured correctly, LiteLLM redirects you out to your corporate login screen. Once you sign in there, it safely bounces you back directly into the full LiteLLM Admin Dashboard.


