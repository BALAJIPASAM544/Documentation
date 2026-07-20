from google.adk.agents import Agent
from .optimization_agent_prompt import Optimization_Agent_Prompt
from dotenv import load_dotenv

load_dotenv()
optimization_agent = Agent(
    name="optimization_agent", 
    model="gemini-2.0-flash",
    description="detects optimization opportunities in source code snippets",
    instruction=Optimization_Agent_Prompt,
    tools=[],
)