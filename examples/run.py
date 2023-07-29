import os
from pprint import pprint
from pdx import Agent
from pdx.utils.rw import read_yaml
from pdx.settings import process

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
agent_name = 'text_agent'
completion_agent = Agent(path=os.path.join(FILE_PATH, agent_name))
test_case = read_yaml(os.path.join(
    FILE_PATH, agent_name, 'tests', 'test_1.yaml'))

process.verbose = True

if __name__ == '__main__':
    _r = completion_agent.execute(test_case)
    # pprint(_r)
    # pprint(repr(_r))
    pprint(_r.model_dump())
