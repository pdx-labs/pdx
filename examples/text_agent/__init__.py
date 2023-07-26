import os
from pdx import Agent, Completion, Prompt, Model
Prompt(content, template, role, pointer)
Model(config)
Completion(prompt, model)
Agent(tool=Completion, model=Model)


text_agent = Agent(os.path.dirname(__file__))

if __name__ == '__main__':
    _question = 'What are the uses of Glucose?'

    _response = text_agent.execute({
        '1_prompt': {'question': _question}
    })

    print(_response.completion)