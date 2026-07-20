from google.adk.agents import Agent
from .best_practice_prompt import Best_Practice_Agent_Prompt
from dotenv import load_dotenv

load_dotenv()
best_practice_agent = Agent(
    name="best_practice_agent", 
    model="gemini-2.0-flash",
    description="reviews code quality and coding standards",
    instruction=Best_Practice_Agent_Prompt,
    tools=[],
)