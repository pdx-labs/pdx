from pprint import pprint
from dataclasses import asdict
from pdx import Worker, Prompt
from pdx.prompt.prompt_chain import PromptChain
from pdx.models.openai import CompletionsModel as OpenAICompletionModel
from pdx.settings import Keys

keys = Keys()

prompt_1 = Prompt("Complete this sentence: ")

prompt_2_system = Prompt(template="This is a system prompt. You are a {{role}}.",
                         role="system", pointer="system")
prompt_2_user = Prompt(template="Based on your role, answer my question in steps. Question is {{question}}.",
                       role="user", pointer="user_0")
prompt_chain = PromptChain([prompt_2_system, prompt_2_user])

completion_model = OpenAICompletionModel(
    api_key=keys.openai_key, model='text-davinci-003')

# text_agent = Agent(os.path.dirname(__file__))

if __name__ == '__main__':
    _role = 'Chemist'
    _question = 'What are the uses of Glucose?'

    # completions_worker = Worker(prompt_1)
    completion_worker = Worker(prompt_chain, completion_model)
    _r = completion_worker.execute({
        'system': {'role': _role},
        'user_0': {'question': _question},
    })
    pprint(_r.data)
    pprint(asdict(_r))
