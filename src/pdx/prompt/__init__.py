from pdx.prompt.prompt_template import PromptTemplate


class Prompt:
    def __init__(self, content: str = None, template: str = None, template_path: str = None, role: str = None, pointer: str = None):
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
            if pointer == None:
                raise Exception('Prompt template must have a pointer.')
            self.pointer = pointer
        elif template_path != None:
            self._prompt = PromptTemplate(
                template_path=template_path, name=pointer)
            if pointer == None:
                raise Exception('Prompt template must have a pointer.')
            self.pointer = pointer

        self.role = role

    def execute(self, values: dict = {}) -> str:
        if isinstance(self._prompt, str):
            return self._prompt
        elif isinstance(self._prompt, PromptTemplate):
            return self._prompt.execute(values)
        else:
            raise Exception('Prompt not initialized properly.')
