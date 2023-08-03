import os
import pytest
from pdx import Agent, Prompt
from pdx.agent.metadata import AgentID, AgentResponse
from pdx.models.metadata import ModelResponse
from pdx.models.openai.completion import CompletionModel
from pdx.models.openai.image.generation import ImageGenerationModel


class TestConfig():
    prompt_template = "An {{subject}} in photorealistic style."
    request_values = {'subject': 'astronaut riding a horse'}
    openai_key = os.environ['OPENAI_API_KEY']
    prompt: Prompt = None
    model: ImageGenerationModel = None
    agent: Agent = None


@pytest.fixture
def config():
    _config = TestConfig()
    _config.prompt = Prompt(template=_config.prompt_template)
    _config.model = ImageGenerationModel(
        api_key=_config.openai_key,
        response_format='b64_json'
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


def test_exceptions(request, config: TestConfig):
    # TODO: Add tests for exceptions
    pass
