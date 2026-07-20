class CoordinatorAgent:
    def __init__(self, agents: dict):
        self.agents = agents

    def run(self, task: str) -> dict:
        results = {}
        for name, agent in self.agents.items():
            results[name] = agent.run(task)
        return results
