from pdx import Agent, Completion, Prompt, Model

Prompt(content, template, template_path, role, pointer)
Model(config)
Completion(prompt, model)

prompt_1 = Prompt("Complete this sentence: ")
prompt_2 = Prompt(template="the jinja string", role="the role", pointer="the pointer")
prompt_3 = Prompt(template_path="the jinja string", role="the role", pointer="the pointer")


my_agent = Agent(tool=Completion, model=Model)


text_agent = Agent(os.path.dirname(__file__))

if __name__ == '__main__':
    _question = 'What are the uses of Glucose?'

    _response = text_agent.execute({
        '1_prompt': {'question': _question}
    })

    print(_response.completion)
