import os
import pytest
from pdx import Agent, Prompt
from pdx.agent.metadata import AgentResponse
from pdx.models.metadata import ModelResponse
from pdx.models.replicate.prediction import PredictionModel


class TestConfig():
    prompt_template = "Tell me a joke about {{topic}}."
    request_values = {'topic': 'databases'}
    openai_key = os.environ['REPLICATE_API_KEY']
    prompt: Prompt = None
    model: PredictionModel = None
    agent: Agent = None


@pytest.fixture
def config():
    _config = TestConfig()
    _config.prompt = Prompt(template=_config.prompt_template)
    _config.model = PredictionModel(
        api_key=_config.openai_key,
        model='6ab580ab4eef2c2b440f2441ec0fc0ace5470edaf2cbea50b8550aec0b3fbd38',
        poll_interval=4,
    )
    _config.agent = Agent(prompt=_config.prompt, model=_config.model)

    return _config


def test_execute(request, config: TestConfig):
    _prompt_session = config.prompt.execute(config.request_values)
    _response = config.model.execute(_prompt_session)
    assert isinstance(_response, ModelResponse)
    # assert isinstance(_response.data, str)


def test_agent_execute(request, config: TestConfig):
    _response = config.agent.execute(config.request_values)
    assert isinstance(_response, AgentResponse)
    # assert isinstance(_response.data, str)


@pytest.mark.asyncio
async def test_async_execute(request, config: TestConfig):
    _prompt_session = config.prompt.execute(config.request_values)
    _response = await config.model.aexecute(_prompt_session)
    assert isinstance(_response, ModelResponse)
    # assert isinstance(_response.data, str)


@pytest.mark.asyncio
async def test_async_agent_execute(request, config: TestConfig):
    _response = await config.agent.aexecute(config.request_values)
    assert isinstance(_response, AgentResponse)
    # assert isinstance(_response.data, str)


def test_exceptions(request, config: TestConfig):
    # TODO: Add tests for exceptions
    pass
