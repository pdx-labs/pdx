import os
import pytest
from pdx import Agent, Prompt
from pdx.agent.metadata import AgentResponse
from pdx.models.metadata import ModelResponse
from pdx.models.openai.completion import CompletionModel


class TestConfig():
    prompt_template = "Tell me a joke about {{topic}}."
    request_values = {'topic': 'databases'}
    openai_key = os.environ['OPENAI_API_KEY']
    prompt: Prompt = None
    model: CompletionModel = None
    agent: Agent = None


@pytest.fixture
def config():
    _config = TestConfig()
    _config.prompt = Prompt(template=_config.prompt_template)
    _config.model = CompletionModel(
        api_key=_config.openai_key,
        model='gpt-3.5-turbo'
    )
    _config.agent = Agent(prompt=_config.prompt, model=_config.model)

    return _config


def test_execute(request, config: TestConfig):
    _prompt_session = config.prompt.execute(config.request_values)
    _response = config.model.execute(_prompt_session)
    assert isinstance(_response, ModelResponse)
    assert isinstance(_response.data, str)


def test_agent_execute(request, config: TestConfig):
    _response = config.agent.execute(config.request_values)
    assert isinstance(_response, AgentResponse)
    assert isinstance(_response.data, str)


@pytest.mark.asyncio
async def test_async_execute(request, config: TestConfig):
    _prompt_session = config.prompt.execute(config.request_values)
    _response = await config.model.aexecute(_prompt_session)
    assert isinstance(_response, ModelResponse)
    assert isinstance(_response.data, str)


@pytest.mark.asyncio
async def test_async_agent_execute(request, config: TestConfig):
    _response = await config.agent.aexecute(config.request_values)
    assert isinstance(_response, AgentResponse)
    assert isinstance(_response.data, str)


def test_exceptions(request, config: TestConfig):
    # TODO: Add tests for exceptions
    pass
