from typing import List
from pdx.prompt import Prompt
from pdx.prompt.prompt_session import PromptSession, PromptSessionItem


class PromptChain:
    def __init__(self, prompts: List[Prompt] = None):
        for _prompt in prompts:
            if _prompt.pointer == None:
                raise ValueError(
                    'Prompt Pointer missing.'
                    'PromptChain must be initialized with a list of Prompt objects that have a unique `pointer` property.'
                )
        self._chain = prompts

    def execute(self, values: dict = {}):
        _session_type = None
        _prompt_session = PromptSession()
        for _prompt in self._chain:
            prompt_pointer_request = values.get(_prompt.pointer, {})
            _session_item = _prompt.execute(
                prompt_pointer_request, _output_item=True)

            if _session_type == None:
                if _session_item.role == 'template':
                    _session_type = 'text'
                else:
                    _session_type = 'chat'
            else:
                if _session_type == 'text' and _session_item.role != 'template':
                    raise ValueError(
                        'Cannot mix chat and text prompts in a chain.')
                elif _session_type == 'chat' and _session_item.role == 'template':
                    raise ValueError(
                        'Cannot mix chat and text prompts in a chain.')

            _prompt_session.items.append(_session_item)

        return _prompt_session
