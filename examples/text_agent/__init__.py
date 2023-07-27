import os
from pdx import Agent


text_agent = Agent(os.path.dirname(__file__))

if __name__ == '__main__':
    _question = 'What are the uses of Glucose?'

    _response = text_agent.execute({
        '1_prompt': {'question': _question}
    })

    print(_response.data)
