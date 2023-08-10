import os
from typing import List, Union, Optional, Dict, Any
from pydantic import BaseModel, Field


class PromptSessionItem(BaseModel):
    content: Any
    content_type: str = Field(default='text')
    role: Optional[str] = Field(default=None)
    metadata: Optional[Dict[str, Any]] = Field(default=None)


class PromptSession:
    def __init__(self):
        self.items: List[PromptSessionItem] = []
        self.session_type = None  # text, chat, multimodal
        self.multimodal_items: Dict[str, List[PromptSessionItem]] = {
            'audio': [], 'image': []}

    def __str__(self):
        return f"{self.items}"

    def __repr__(self):
        return f"{self.items}"

    def add(self, session_item: PromptSessionItem):
        if self.session_type == None:
            if session_item.role in ['image', 'audio']:
                self.session_type = 'multimodal'
            elif session_item.role == 'template':
                self.session_type = 'text'
            else:
                self.session_type = 'chat'
        else:
            if self.session_type == 'multimodal' or session_item.role in ['image', 'audio']:
                self.session_type = 'multimodal'
            elif self.session_type == 'text' and session_item.role != 'template':
                raise ValueError(
                    'Cannot mix chat and text prompts in a chain.')
            elif self.session_type == 'chat' and session_item.role == 'template':
                raise ValueError(
                    'Cannot mix chat and text prompts in a chain.')

        if session_item.content_type == 'text':
            self.items.append(session_item)
        elif session_item.content_type == 'image':
            self.multimodal_items['image'].append(session_item)
        elif session_item.content_type == 'audio':
            self.multimodal_items['audio'].append(session_item)
        else:
            raise ValueError(
                f"PromptSessionItem content_type {session_item.content_type} not supported.")

    def audio_prompt(self):
        if len(self.multimodal_items['audio']) == 0:
            raise ValueError('No audio prompt found in PromptSession.')
        _prompt_list = []
        for _item in self.multimodal_items['audio']:
            _file_name = os.path.basename(
                _item.metadata.get('file_path', 'audio.mp3'))
            _content = _item.content
            _prompt_list.append((_file_name, _content))
        return _prompt_list
    
    def image_prompt(self):
        if len(self.multimodal_items['image']) == 0:
            raise ValueError('No image prompt found in PromptSession.')
        _prompt_list = []
        for _item in self.multimodal_items['image']:
            _file_name = os.path.basename(
                _item.metadata.get('file_path', 'image.png'))
            _content = _item.content
            _prompt_list.append((_file_name, _content))
        return _prompt_list

    def text_prompt(self, role_constants: dict = {
        'user': '\n\nUSER',
        'assistant': '\n\nASSISTANT',
        'system': '\n\nSYSTEM'
    }):
        _prompt = ''
        if role_constants != {}:
            _prompt += f"{role_constants.get('user', '')} "

        for item in self.items:
            if item.role in role_constants:
                _prompt += f"{role_constants.get(item.role, '')} {item.content}"
            else:
                _prompt += f"{item.content} "

        if role_constants != {}:
            _prompt += f"{role_constants.get('assistant', '')} "

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
