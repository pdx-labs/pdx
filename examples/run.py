import os
from pprint import pprint
from pdx import Agent

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

completion_agent = Agent(path=os.path.join(FILE_PATH, 'text_agent'))

if __name__ == '__main__':
    pprint(completion_agent)
    pprint(completion_agent._agent_id)
    pprint(completion_agent._config.model_config)
    pprint(completion_agent._model)
    pprint(completion_agent._prompt)
