import os
from typing import Union
from pdx.prompt.prompt_template import PromptTemplate
from pdx.prompt.prompt_session import PromptSession, PromptSessionItem


class Prompt:
    def __init__(self, content: str = None, template: str = None, template_path: str = None, role: str = 'template', pointer: str = 'prompt', file: str = None):
        if file == None:
            if content != None and template != None:
                raise Exception(
                    'Prompt cannot have both content and template.')
            if content != None and template_path != None:
                raise Exception(
                    'Prompt cannot have both content and template_path.')
            if template != None and template_path != None:
                raise Exception(
                    'Prompt cannot have both template and template_path.')
            self.role = role
        elif file != None:
            if os.path.isfile(file):
                self.file_content = open(file, 'rb')
                file_name = os.path.basename(file)
                self.file_path = os.path.abspath(file)
                self.pointer = file_name.split(sep=".")[0]
                self.file_extension = file_name.split(sep=".")[-1]
                if self.file_extension.lower() in ['png']:
                    self.prompt_type = 'image'
                    self.role = 'image'
                elif self.file_extension.lower() in ['mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'wav', 'webm']:
                    self.prompt_type = 'audio'
                    self.role = 'audio'
                # elif self.file_extension.lower() in ['mp4', 'mov', 'avi']:
                #     self.prompt_type = 'video'
                else:
                    raise Exception(
                        'File type not supported. Check the list of support file types.')
            else:
                raise Exception('Prompt file not found or does not exist.')
        else:
            raise Exception('Prompt not initialized properly.')

        if content != None:
            self._prompt = content
            self.pointer = pointer
            self.prompt_type = 'text'
        elif template != None:
            self._prompt = PromptTemplate(
                template_string=template, name=pointer)
            self.pointer = pointer
            self.prompt_type = 'text'
        elif template_path != None:
            self._prompt = PromptTemplate(
                template_path=template_path, name=pointer)
            self.pointer = pointer
            self.prompt_type = 'text'

    def execute(self, values: dict = {}, _output_item=False, prompt_session: PromptSession = None) -> Union[PromptSession, PromptSessionItem]:
        if self.prompt_type in ['image', 'audio']:
            _prompt_content = self.file_content
            _metadata = {'file_path': self.file_path}
        elif isinstance(self._prompt, str):
            _prompt_content = self._prompt
            _metadata = None
        elif isinstance(self._prompt, PromptTemplate):
            _prompt_content = self._prompt.execute(values)
            _metadata = None
        else:
            raise Exception('Prompt not initialized properly.')

        prompt_session_item = PromptSessionItem(
            content=_prompt_content,
            role=self.role,
            content_type=self.prompt_type,
            metadata=_metadata)

        if _output_item:
            return prompt_session_item
        elif prompt_session is not None:
            prompt_session.add(prompt_session_item)
        else:
            _prompt_session = PromptSession()
            _prompt_session.add(prompt_session_item)
            return _prompt_session
