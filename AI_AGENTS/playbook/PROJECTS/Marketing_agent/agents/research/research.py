import google.adk.agents

research_agent = google.adk.agents.Agent(
    name="research_agent",
    model="gemini-2.0-flash",
    description="A market research agent that analyzes products and returns structured insights.",
    instruction="""Analyze the given product and return a well-structured market research report using the following format:

## Market Research Report

**Industry:** <industry name>

**Target Audience:**
- <audience segment 1>
- <audience segment 2>

**Top Competitors:**
- <competitor 1>
- <competitor 2>
- <competitor 3>

**Pain Points:**
- <pain point 1>
- <pain point 2>

**Opportunities:**
- <opportunity 1>
- <opportunity 2>

Use bullet points and bold headers. Be concise and specific to the product provided.""",
)
