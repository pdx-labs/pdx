from dataclasses import dataclass
from typing import List, Union, Dict
from pdx.prompt import Prompt
from pdx.prompt.prompt_chain import PromptChain
from pdx.prompt.prompt_tree import PromptTree


@dataclass
class PromptSessionItem:
    content: str
    content_type: str = 'text'
    role: str = None


class PromptSession:
    def __init__(self):
        self.items: List[PromptSessionItem] = []
        self.session_type = 'text'  # text, chat

    def add(self, content: str, role: str = None, content_type: str = 'text'):
        self.items.append(PromptSessionItem(
            content=content, content_type=content_type, role=role))

    def execute(self, prompt: Union[Prompt, PromptChain, PromptTree], request: Dict):
        if isinstance(prompt, Prompt):
            prompt_pointer_request = request.get(prompt.pointer, {})
            content = prompt.execute(prompt_pointer_request)
            self.add(content=content, role=prompt.role)
        elif isinstance(prompt, PromptChain):
            for _prompt in prompt._chain:
                prompt_pointer_request = request.get(_prompt.pointer, {})
                content = _prompt.execute(prompt_pointer_request)
                self.add(content=content, role=_prompt.role)
        elif isinstance(prompt, PromptTree):
            raise Exception('PromptTree not implemented.')

    def text_prompt(self, role_constants: dict = {
        'user': '\n\nUSER',
        'assistant': '\n\nASSISTANT',
        'system': '\n\nSYSTEM'
    }):
        _prompt = ''
        for item in self.items:
            if item.role in role_constants:
                _prompt += f"{role_constants.get(item.role, '')} {item.content}"
            else:
                _prompt += f"{item.content} "

        if role_constants != {}:
            _prompt += f"{role_constants.get('assistant', '')}"

        return _prompt

    def chat_prompt(self):
        _prompt_dict_list = []
        for item in self.items:
            _prompt_dict_list.append({
                'role': item.role,
                'content': item.content
            })
        return _prompt_dict_list

    def export(self):
        _prompt_dict_list = []
        for item in self.items:
            _prompt_dict_list.append({
                'role': item.role,
                'content': item.content
            })
        return _prompt_dict_list
