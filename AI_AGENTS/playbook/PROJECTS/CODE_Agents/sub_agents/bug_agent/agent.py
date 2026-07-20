from google.adk.agents import Agent
from .bug_agent_prompt import BUG_AGENT_PROMPT
from dotenv import load_dotenv

load_dotenv()
bug_agent = Agent(
    name="bug_agent", 
    model="gemini-2.0-flash",
    description="detects bugs in source code snippets",
    instruction=BUG_AGENT_PROMPT,
    tools=[],
)