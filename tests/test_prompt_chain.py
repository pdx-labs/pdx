import os
import pytest
from pdx.prompt import Prompt
from pdx.prompt.prompt_chain import PromptChain
from pdx.prompt.prompt_session import PromptSession, PromptSessionItem


class TestConfig():
    system_1: str = "{{compound}} is {{description}}."
    system_1_context: dict = {"compound": "Glucose", "description": "a sugar"}
    user_1: str = "What is {{compound}}?"
    user_1_context: dict = {"compound": "Glucose"}
    template: str = "{{compound}} is {{description}}. What is {{compound}}?"
    template_context: dict = {"compound": "Glucose", "description": "a sugar"}
    prompt_output: str = "Glucose is a sugar. What is Glucose?"
    audio_file: str = os.path.join(os.path.dirname(
        __file__), 'assets/test_prompt_chain_multimodal.wav')


@pytest.fixture
def config():
    _config = TestConfig()
    return _config


def test_template_prompt(config: TestConfig):
    prompt = Prompt(template=config.template, pointer='template')
    _response = prompt.execute(config.template_context)
    assert isinstance(_response, PromptSession)
    assert _response.session_type == 'text'
    assert len(_response.items) == 1
    assert isinstance(_response.items, list)
    assert isinstance(_response.items[0], PromptSessionItem)
    assert _response.items[0].content == config.prompt_output


def test_prompt_chain_text(config: TestConfig):
    prompt_system = Prompt(template=config.system_1, pointer='system')
    prompt_user = Prompt(template=config.user_1, pointer='user')
    prompt_chain = PromptChain(prompts=[prompt_system, prompt_user])
    _response = prompt_chain.execute({
        'system': config.system_1_context,
        'user': config.user_1_context
    })
    assert isinstance(_response, PromptSession)
    assert _response.session_type == 'text'
    assert len(_response.items) == 2
    assert isinstance(_response.items, list)
    assert isinstance(_response.items[0], PromptSessionItem)
    assert isinstance(_response.items[1], PromptSessionItem)
    assert isinstance(_response.text_prompt({}), str)


def test_prompt_chain_chat(config: TestConfig):
    prompt_system = Prompt(template=config.system_1,
                           pointer='system', role='system')
    prompt_user = Prompt(template=config.user_1, pointer='user', role='user')
    prompt_chain = PromptChain(prompts=[prompt_system, prompt_user])
    _response = prompt_chain.execute({
        'system': config.system_1_context,
        'user': config.user_1_context
    })
    assert isinstance(_response, PromptSession)
    assert _response.session_type == 'chat'
    assert len(_response.items) == 2
    assert isinstance(_response.items, list)
    assert isinstance(_response.items[0], PromptSessionItem)
    assert isinstance(_response.items[1], PromptSessionItem)
    assert isinstance(_response.text_prompt({}), str)


def test_prompt_chain_multimodal(config: TestConfig):
    text_prompt = Prompt(template=config.template, pointer='template')
    audio_prompt = Prompt(file=config.audio_file)
    prompt_chain = PromptChain(prompts=[text_prompt, audio_prompt])
    _response = prompt_chain.execute({
        'template': config.template_context,
    })
    assert isinstance(_response, PromptSession)
    assert _response.session_type == 'multimodal'
    assert isinstance(_response.items, list)
    assert len(_response.items) == 1
    assert isinstance(_response.items[0], PromptSessionItem)
    assert isinstance(_response.multimodal_items, dict)
    assert isinstance(_response.multimodal_items['audio'], list)
    assert len(_response.multimodal_items['audio']) == 1
    assert isinstance(
        _response.multimodal_items['audio'][0], PromptSessionItem)
    assert isinstance(_response.text_prompt({}), str)
    assert isinstance(_response.audio_prompt(), bytes)
