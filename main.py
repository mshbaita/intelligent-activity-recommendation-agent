from agent import RecommendationAgent
import os
import openai
from utils.config import config

os.environ["OPENAI_API_KEY"] = config.OPENAI_API_KEY
openai.api_key = config.OPENAI_API_KEY
os.environ["SERPAPI_API_KEY"] = config.SERPAPI_API_KEY

if __name__ == '__main__':
    print("Intro message")
    print("-" * 50)
    agent = RecommendationAgent()
    while True:
        user_message = input(f"User: ")
        agent_response = agent.execute(user_message)
        print(f"Agent: {agent_response}")
