from google.adk.agents import Agent
from .documentation_agent_prompt import documentation_agent_prompt
from dotenv import load_dotenv
load_dotenv()
documentation_agent = Agent(
    name="documentation_agent", 
    model="gemini-2.0-flash",
    description="generates technical documentation",
    instruction=documentation_agent_prompt ,
    tools=[],
)