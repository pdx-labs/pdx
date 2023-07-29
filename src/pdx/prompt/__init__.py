from typing import Union
from pdx.prompt.prompt_template import PromptTemplate
from pdx.prompt.prompt_session import PromptSession, PromptSessionItem


class Prompt:
    def __init__(self, content: str = None, template: str = None, template_path: str = None, role: str = 'template', pointer: str = None):
        if content != None and template != None:
            raise Exception('Prompt cannot have both content and template.')
        if content != None and template_path != None:
            raise Exception(
                'Prompt cannot have both content and template_path.')
        if template != None and template_path != None:
            raise Exception(
                'Prompt cannot have both template and template_path.')

        if content != None:
            self._prompt = content
            self.pointer = pointer
        elif template != None:
            self._prompt = PromptTemplate(
                template_string=template, name=pointer)
            self.pointer = pointer
        elif template_path != None:
            self._prompt = PromptTemplate(
                template_path=template_path, name=pointer)
            self.pointer = pointer

        self.role = role

    def execute(self, values: dict = {}, _output_item=False, prompt_session: PromptSession = None) -> Union[PromptSession, PromptSessionItem]:
        _prompt_content = ''
        if isinstance(self._prompt, str):
            _prompt_content = self._prompt
        elif isinstance(self._prompt, PromptTemplate):
            _prompt_content = self._prompt.execute(values)
        else:
            raise Exception('Prompt not initialized properly.')

        if _output_item:
            return PromptSessionItem(content=_prompt_content, role=self.role)
        elif prompt_session is not None:
            prompt_session.add(content=_prompt_content, role=self.role)
        else:
            _prompt_session = PromptSession()
            if self.role != 'template':
                _prompt_session.session_type == 'chat'
            else:
                _prompt_session.session_type == 'text'
            _prompt_session.add(content=_prompt_content, role=self.role)
            return _prompt_session
