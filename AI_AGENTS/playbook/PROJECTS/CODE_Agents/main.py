import asyncio
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from root_agent.agent import root_agent

load_dotenv()
APP_NAME = "root_agent"
USER_ID = "user_123"
SESSION_ID = "session_123"

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

sample_code = """
def divide(a,b):
    return a/b

print(divide(10,0))
"""

user_message = types.Content(
    role="user",
    parts=[types.Part(text=f"Review this code:\n{sample_code}")],
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
        print("=" * 60)
        print("AUTHOR:", event.author)
        if event.content and event.content.parts:
            print("MESSAGE:", event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(main())
