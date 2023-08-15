import os
import pytest
from pdx import Agent, Prompt, PromptChain
from pdx.settings import process
from pdx.agent.metadata import AgentResponse
from pdx.models.metadata import ModelResponse
from pdx.models.stability.image.variation import ImageVariationModel

process.verbose = True
process._release = False

ASSETS_FOLDER = os.path.join(os.path.dirname(
    os.path.dirname(os.path.dirname(__file__))), 'assets')
FILE_NAME = 'image.png'
FILE_PATH = os.path.join(ASSETS_FOLDER, FILE_NAME)


class TestConfig():
    prompt_1 = "a close view of the mountains"
    weight_1 = 1
    prompt_2 = "houses in the mountains"
    weight_2 = -1
    api_key = os.environ['STABILITY_API_KEY']
    prompt: Prompt = None
    model: ImageVariationModel = None
    agent: Agent = None


@pytest.fixture
def config():
    _config = TestConfig()
    _pi = Prompt(file=FILE_PATH)
    _pp = Prompt(_config.prompt_1, metadata={'weight': _config.weight_1}, pointer='p_1')
    _pn = Prompt(_config.prompt_2, metadata={'weight': _config.weight_2}, pointer='p_2')
    _config.prompt = PromptChain([_pi, _pp, _pn])
    _config.model = ImageVariationModel(
        api_key=_config.api_key,
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
