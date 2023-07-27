import os
from pprint import pprint
from pdx import Agent
from pdx.utils.rw import read_yaml

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
agent_name = 'text_agent'
completion_agent = Agent(path=os.path.join(FILE_PATH, agent_name))
test_case = read_yaml(os.path.join(
    FILE_PATH, agent_name, 'tests', 'test_1.yaml'))

if __name__ == '__main__':
    pprint(completion_agent.execute(test_case))
    
