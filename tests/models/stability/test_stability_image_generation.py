import os
import pytest
from pdx import Agent, Prompt
from pdx.settings import process
from pdx.agent.metadata import AgentResponse
from pdx.models.metadata import ModelResponse
from pdx.models.stability.image.generation import ImageGenerationModel

process.verbose = True
process._release = False


class TestConfig():
    prompt_template = "{{aubject}}, add magic touch fine art realism, storybook illustrations, grainy, classic portraiture, golden light."
    request_values = {
        'subject': 'view of the dolomites, showing three peaks of the tre cime in the distance'}
    api_key = os.environ['STABILITY_API_KEY']
    prompt: Prompt = None
    model: ImageGenerationModel = None
    agent: Agent = None


@pytest.fixture
def config():
    _config = TestConfig()
    _config.prompt = Prompt(template=_config.prompt_template)
    _config.model = ImageGenerationModel(
        api_key=_config.api_key,
    )
    _config.agent = Agent(prompt=_config.prompt, model=_config.model)

    return _config


def test_execute(request, config: TestConfig):
    _prompt_session = config.prompt.execute(config.request_values)
    _response = config.model.execute(_prompt_session)
    assert isinstance(_response, ModelResponse)
    assert isinstance(_response.data, bytes)


def test_agent_execute(request, config: TestConfig):
    _response = config.agent.execute(config.request_values)
    assert isinstance(_response, AgentResponse)
    assert isinstance(_response.data, bytes)


@pytest.mark.asyncio
async def test_async_execute(request, config: TestConfig):
    _prompt_session = config.prompt.execute(config.request_values)
    _response = await config.model.aexecute(_prompt_session)
    assert isinstance(_response, ModelResponse)
    assert isinstance(_response.data, bytes)


@pytest.mark.asyncio
async def test_async_agent_execute(request, config: TestConfig):
    _response = await config.agent.aexecute(config.request_values)
    assert isinstance(_response, AgentResponse)
    assert isinstance(_response.data, bytes)


def test_exceptions(request, config: TestConfig):
    # TODO: Add tests for exceptions
    pass
