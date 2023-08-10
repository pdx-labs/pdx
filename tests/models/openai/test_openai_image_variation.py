import os
import pytest
from pdx import Agent, Prompt
from pdx.agent.metadata import AgentResponse
from pdx.models.metadata import ModelResponse
from pdx.models.openai.image.variation import ImageVariationModel

ASSETS_FOLDER = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), 'assets')
FILE_NAME = 'image.png'
FILE_PATH = os.path.join(ASSETS_FOLDER, FILE_NAME)


class TestConfig():
    openai_key = os.environ['OPENAI_API_KEY']
    prompt: Prompt = None
    model: ImageVariationModel = None
    agent: Agent = None


@pytest.fixture
def config():
    _config = TestConfig()
    _config.prompt = Prompt(file=FILE_PATH)
    _config.model = ImageVariationModel(
        api_key=_config.openai_key,
        response_format='b64_json'
    )
    _config.agent = Agent(prompt=_config.prompt, model=_config.model)

    return _config


def test_execute(request, config: TestConfig):
    _prompt_session = config.prompt.execute()
    _response = config.model.execute(_prompt_session)
    assert isinstance(_response, ModelResponse)
    assert isinstance(_response.data, bytes)


def test_agent_execute(request, config: TestConfig):
    _response = config.agent.execute()
    assert isinstance(_response, AgentResponse)
    assert isinstance(_response.data, bytes)


@pytest.mark.asyncio
async def test_async_execute(request, config: TestConfig):
    _prompt_session = config.prompt.execute()
    _response = await config.model.aexecute(_prompt_session)
    assert isinstance(_response, ModelResponse)
    assert isinstance(_response.data, bytes)


@pytest.mark.asyncio
async def test_async_agent_execute(request, config: TestConfig):
    _response = await config.agent.aexecute()
    assert isinstance(_response, AgentResponse)
    assert isinstance(_response.data, bytes)


def test_exceptions(request, config: TestConfig):
    # TODO: Add tests for exceptions
    pass
