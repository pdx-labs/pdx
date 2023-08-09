import os
import asyncio
from pdx import Agent, Prompt
from pdx.models.openai import CompletionModel as OpenAICompletionModel
from pdx.models.anthropic import CompletionModel as AnthropicCompletionModel
from pdx.models.cohere import GenerationModel as CohereCompletionModel
from pdx.settings import process

process.verbose = True

prompt = Prompt(template="Tell me a joke about {{topic}}.")
openai_model = OpenAICompletionModel(
    api_key=os.environ['OPENAI_KEY'], model='text-davinci-003')
anthropic_model = AnthropicCompletionModel(
    api_key=os.environ['ANTHROPIC_KEY'], model='claude-1')
cohere_model = CohereCompletionModel(
    api_key=os.environ['COHERE_KEY'], model='command')


def main():
    agents = [
        Agent(prompt=prompt, model=openai_model),
        Agent(prompt=prompt, model=anthropic_model),
        Agent(prompt=prompt, model=cohere_model)
    ]

    request_values = {'topic': 'dogs'}

    for agent in agents:
        print('\nTest response:')
        _r = agent.execute(request_values)
        print(_r.data)
        print('\n\n')


async def amain():
    agent_openai = Agent(prompt=prompt, model=openai_model)
    agent_anthropic = Agent(prompt=prompt, model=anthropic_model)
    agent_cohere = Agent(prompt=prompt, model=cohere_model)

    request_values = {'topic': 'dogs'}

    L = await asyncio.gather(
        agent_openai.aexecute(request_values),
        agent_anthropic.aexecute(request_values),
        agent_cohere.aexecute(request_values)
    )

    for _response in L:
        print('\nTest response:')
        print(_response.data)
        print('\n\n')


if __name__ == '__main__':
    # asyncio.run(amain())
    # main()
    pass
