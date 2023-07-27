import os
from pprint import pprint
from pdx import Agent

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

completion_agent = Agent(path=os.path.join(FILE_PATH, 'chat_agent'))

if __name__ == '__main__':
    prompt_tree = completion_agent._prompt
    # prompt_session = prompt_tree.execute({})
    # pprint(prompt_session)
    
