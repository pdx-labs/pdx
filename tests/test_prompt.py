import os
import pytest
from typing import List
from pdx.prompt import Prompt
from pdx.prompt.prompt_session import PromptSession, PromptSessionItem


ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")


class TestConfig():
    basic_prompt: str = "What are the uses of Glucose?"
    template: str = "What are the uses of {{compound}}?"
    template_path: str = f"{ASSETS_PATH}/prompt_template.jinja"
    pointer: str = "1_prompt"
    template_context: dict = {"compound": "Glucose"}
    prompt_output: str = "What are the uses of Glucose?"


@pytest.fixture
def config():
    _config = TestConfig()
    return _config


def test_basic_prompt(config: TestConfig):
    prompt = Prompt(content=config.basic_prompt)
    _response = prompt.execute()
    assert isinstance(_response, PromptSession)
    assert len(_response.items) == 1
    assert isinstance(_response.items, List)
    assert isinstance(_response.items[0], PromptSessionItem)
    assert _response.items[0].content == config.prompt_output


def test_template_prompt(config: TestConfig):

    prompt = Prompt(template=config.template, pointer=config.pointer)
    _response = prompt.execute(config.template_context)
    assert isinstance(_response, PromptSession)
    assert len(_response.items) == 1
    assert isinstance(_response.items, List)
    assert isinstance(_response.items[0], PromptSessionItem)
    assert _response.items[0].content == config.prompt_output


def test_template_path_prompt(config: TestConfig):

    prompt = Prompt(template_path=config.template_path, pointer=config.pointer)
    _response = prompt.execute(config.template_context)
    assert isinstance(_response, PromptSession)
    assert len(_response.items) == 1
    assert isinstance(_response.items, List)
    assert isinstance(_response.items[0], PromptSessionItem)
    assert _response.items[0].content == config.prompt_output
