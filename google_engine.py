import os
from abc import abstractmethod

from langchain import OpenAI
from langchain.agents import initialize_agent, load_tools, AgentType


class GoogleSearch:
    def __init__(self):
        self._validate_environment()

    @abstractmethod
    def _validate_environment(self):
        if not os.getenv("SERPAPI_API_KEY"):
            raise Exception("No SERPAPI API key found")

    def __call__(self, query, **kwargs):
        llm = OpenAI(temperature=0)
        tools = load_tools(["serpapi"], llm=llm)
        agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
        return agent.run(query)




