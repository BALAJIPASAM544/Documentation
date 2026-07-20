import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.research.research import research_agent

load_dotenv()
APP_NAME = "marketing_agent"
USER_ID = "user_123"
SESSION_ID = "session_123"

session_service=InMemorySessionService()

runner = Runner(
    agent=research_agent,
    app_name=APP_NAME,
    session_service=session_service,
)
#user_message is the message that the user sends to the agent, in this case it is a research request for the product "AI code reviewer"
user_message=types.Content(
    role="user",
    parts=[types.Part(text="Research the product AI code reviewer")],
)


async def main():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=user_message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())