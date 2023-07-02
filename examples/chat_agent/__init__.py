import os
from pdx import Agent

chat_agent = Agent(os.path.dirname(__file__))

if __name__ == '__main__':
    _question = 'What are the uses of Glucose?'

    _response = chat_agent.execute({
        '2_user': {'question': _question}
    })

    print(_response)
