from typing import List
from pdx.prompt import Prompt
from pdx.prompt.prompt_session import PromptSession, PromptSessionItem


class PromptChain:
    def __init__(self, prompts: List[Prompt] = None):
        self._pointers: List[str] = []
        self._chain: List[Prompt] = []
        for _prompt in prompts:
            if _prompt.pointer in self._pointers:
                raise ValueError(
                    'PromptChain must be initialized with a list of Prompt objects that have a unique `pointer` property.'
                )
            else:
                self._pointers.append(_prompt.pointer)
                self._chain.append(_prompt)

    def execute(self, values: dict = {}):
        _prompt_session = PromptSession()
        for _prompt in self._chain:
            prompt_pointer_request = values.get(_prompt.pointer, {})
            _session_item = _prompt.execute(
                prompt_pointer_request, _output_item=True)
            _prompt_session.add(_session_item)

        return _prompt_session
