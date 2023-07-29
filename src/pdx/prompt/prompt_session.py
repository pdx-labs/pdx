from typing import List, Union, Dict, Optional
from pydantic import BaseModel, Field


class PromptSessionItem(BaseModel):
    content: str
    content_type: str = Field(default='text')
    role: Optional[str] = Field(default=None)


class PromptSession:
    def __init__(self):
        self.items: List[PromptSessionItem] = []
        self.session_type = 'text'  # text, chat

    def __str__(self):
        return f"{self.items}"

    def __repr__(self):
        return f"{self.items}"

    def add(self, content: str, role: str = None, content_type: str = 'text'):
        self.items.append(PromptSessionItem(
            content=content, content_type=content_type, role=role))

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
