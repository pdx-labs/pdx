import os
from pdx import Agent

AGENT_FOLDER = TEMPLATES_PATH = os.path.dirname(__file__)

simple_agent = Agent(AGENT_FOLDER)

if __name__ == "__main__":
    response = simple_agent.execute({
        "topic": "The benefits of reading",
        "summary": "Reading is good for your brain. It helps you to think better.",
        "question": "What are the benefits of reading?"
    })

    print(response)
