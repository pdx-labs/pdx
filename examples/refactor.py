from pprint import pprint
from dataclasses import asdict
from pdx import Agent, Worker, Prompt
from pdx.prompt.prompt_chain import PromptChain
from pdx.models.openai import CompletionsModel as OpenAICompletionModel
from pdx.models.anthropic import CompleteModel as AnthropicCompletionModel
from pdx.settings import Keys

keys = Keys()

prompt_1 = Prompt("Complete this sentence: ")

prompt_2_system = Prompt(template="This is a system prompt. You are a {{role}}.",
                         role="system", pointer="system")
prompt_2_user = Prompt(template="Based on your role, answer my question in steps. Question is {{question}}.",
                       role="user", pointer="user_0")
prompt_chain = PromptChain([prompt_2_system, prompt_2_user])

openai_completions = OpenAICompletionModel(
    api_key=keys.openai_key, model='text-davinci-003')
anthropic_completions = AnthropicCompletionModel(
    api_key=keys.anthropic_key, model='claude-v1')

# text_agent = Agent(os.path.dirname(__file__))

if __name__ == '__main__':
    _role = 'Chemist'
    _question = 'What are the uses of Glucose?'

    # pprint(prompt_1.execute())

    # pprint(openai_completions.execute(prompt_chain.execute({
    #     'system': {'role': _role},
    #     'user_0': {'question': _question},
    # })))
    completion_worker = Worker(prompt_chain, anthropic_completions)
    completion_agent = Agent(prompt_chain, anthropic_completions)

    _r = completion_agent.execute({
        'system': {'role': _role},
        'user_0': {'question': _question},
    })
    pprint(_r.data)
    pprint(asdict(_r))
