import os
import pytest
from pdx import Agent, Prompt
from pdx.agent.metadata import AgentID, AgentResponse
from pdx.models.openai import CompletionModel as OpenAICompletionModel
from pdx.models.anthropic import CompletionModel as AnthropicCompletionModel


class TestConfig:
    prompt_template = "Tell me a joke about {{topic}}."
    request_values_1 = {'topic': 'dogs'}
    request_values_2 = {'topic': 'cats'}
    request_values_3 = {'topic': 'birds'}
    openai_key = os.environ['OPENAI_KEY']
    anthropic_key = os.environ['ANTHROPIC_KEY']


@pytest.fixture()
def config():
    return TestConfig()


def test_agent_request(request, config: TestConfig):
    prompt = Prompt(template=config.prompt_template)
    model = OpenAICompletionModel(
        api_key=os.environ['OPENAI_KEY'], model='text-davinci-003')
    agent = Agent(prompt=prompt, model=model)
    _response = agent.execute(config.request_values_1)

    assert isinstance(_response, AgentResponse)
    assert isinstance(_response.data, str)


if __name__ == '__main__':
    _config = TestConfig()

    prompt = Prompt(template=_config.prompt_template)
    model = OpenAICompletionModel(
        api_key=_config.openai_key,
        model='text-davinci-003'
    )
    agent = Agent(prompt=prompt, model=model)
    print(agent.execute(_config.request_values_1).model_dump(mode='json'))
    print(agent.execute(_config.request_values_2).model_dump(mode='json'))
