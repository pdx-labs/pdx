import os
import pytest
import time
from pdx import Agent, Prompt
from pdx.agent.metadata import AgentID, AgentResponse
from pdx.models.openai import CompletionModel as OpenAICompletionModel
from pdx.models.anthropic import CompletionModel as AnthropicCompletionModel
from pdx.cache import InMemoryCache


class TestConfig:
    prompt_template = "Tell me a joke about {{topic}}."
    request_values = {'topic': 'dogs'}
    openai_key = os.environ['OPENAI_KEY']
    anthropic_key = os.environ['ANTHROPIC_KEY']
    prompt: Prompt = None
    model: OpenAICompletionModel = None


@pytest.fixture()
def config():
    _config = TestConfig()
    _config.prompt = Prompt(template=_config.prompt_template)
    _config.model = OpenAICompletionModel(
        api_key=_config.openai_key,
        model='text-davinci-003'
    )

    return _config


def test_in_memory_cache(request, config: TestConfig):
    in_memory_cache = InMemoryCache()
    agent = Agent(prompt=config.prompt, model=config.model,
                  cache=in_memory_cache)
    start = time.time()
    _response_1 = agent.execute(config.request_values)
    first = time.time()
    _response_2 = agent.execute(config.request_values)
    second = time.time()
    _response_3 = agent.execute(config.request_values)
    third = time.time()

    assert isinstance(_response_1, AgentResponse)
    assert isinstance(_response_2, AgentResponse)
    assert isinstance(_response_3, AgentResponse)
    assert _response_1 == _response_2
    assert _response_1.metadata.request.request_id == _response_2.metadata.request.request_id
    assert _response_2.metadata.request.request_id == _response_3.metadata.request.request_id
    assert _response_1.metadata.request.request_id == _response_3.metadata.request.request_id
    assert _response_1.metadata.response.api_log_id == _response_2.metadata.response.api_log_id
    assert _response_2.metadata.response.api_log_id == _response_3.metadata.response.api_log_id
    assert _response_1.metadata.response.api_log_id == _response_3.metadata.response.api_log_id
    assert (first - start) > (second - first)
    assert (first - start) > (third - second)
