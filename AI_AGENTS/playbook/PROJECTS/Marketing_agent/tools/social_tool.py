def post_to_social(platform: str, content: str) -> str:
    return f"[SocialTool] Posted to {platform}: {content[:50]}..."
