import os
import pytest
from pydantic import BaseModel
from pdx.prompt import Prompt, PromptTemplate


ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")


@pytest.fixture
def config():
    class TestConfig(BaseModel):
        basic_prompt: str = "What are the uses of Glucose?"
        template: str = "What are the uses of {{compound}}?"
        template_path: str = f"{ASSETS_PATH}/prompt_template.jinja"
        pointer: str = "1_prompt"
        template_context: dict = {"compound": "Glucose"}
        prompt_output: str = "What are the uses of Glucose?"

    return TestConfig()


def test_basic_prompt(config):

    prompt = Prompt(content=config.basic_prompt)
    _response = prompt.execute()
    assert _response == config.prompt_output


def test_template_prompt(config):

    prompt = Prompt(template=config.template, pointer=config.pointer)
    _response = prompt.execute(config.template_context)
    assert _response == config.prompt_output


def test_template_path_prompt(config):

    prompt = Prompt(template_path=config.template_path, pointer=config.pointer)
    _response = prompt.execute(config.template_context)
    assert _response == config.prompt_output
