from google.adk.agents.llm_agent import Agent


#Mock tool implementation
def get_current_time(city:str)->dict:
    """Returns the current time in a given city."""
    # This is a mock implementation - replace with actual time API call
    return {"city": city, "time": "12:00 PM"}

root_agent = Agent(
    model='gemini-3.5-flash',
    name='root_agent',
    description='Tells the current time in a specified city.',
    instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
    tools=[get_current_time]
)
