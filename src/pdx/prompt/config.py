from typing import List


class PromptConfig:
    def __init__(self, config: List[dict], templates_path: str):
        self.config = config
        self.templates_path = templates_path
        self.prompt_type = None

        self._system_count = 0
        self._validate(self.config)

    def _validate(self, config: dict):
        for _p in config:
            if 'template' in _p:
                if self.prompt_type is None:
                    self.prompt_type = 'text'
                elif self.prompt_type == 'text':
                    pass
                elif self.prompt_type != 'text':
                    raise Exception(
                        f'Prompt type mixing of `template` with `system/user/assistant` detected.')
                else:
                    raise Exception(
                        f'Prompt type mixing of `template` with `system/user/assistant` detected.')

            elif 'system' in _p:
                self._system_count += 1
                if self._system_count > 1:
                    raise Exception(
                        f'Only 1 `system` type prompt can be used.')
                if self.prompt_type is None:
                    self.prompt_type = 'chat'
                elif self.prompt_type == 'chat':
                    pass
                elif self.prompt_type != 'chat':
                    raise Exception(
                        f'Prompt type mixing of `template` with `system/user/assistant` detected.')
                else:
                    raise Exception(
                        f'Prompt type mixing of `template` with `system/user/assistant` detected.')

            elif 'user' in _p:
                if self.prompt_type is None:
                    self.prompt_type = 'chat'
                elif self.prompt_type == 'chat':
                    pass
                elif self.prompt_type != 'chat':
                    raise Exception(
                        f'Prompt type mixing of `template` with `system/user/assistant` detected.')
                else:
                    raise Exception(
                        f'Prompt type mixing of `template` with `system/user/assistant` detected.')

            elif 'assistant' in _p:
                if self.prompt_type is None:
                    self.prompt_type = 'chat'
                elif self.prompt_type == 'chat':
                    pass
                elif self.prompt_type != 'chat':
                    raise Exception(
                        f'Prompt type mixing of `template` with `system/user/assistant` detected.')
                else:
                    raise Exception(
                        f'Prompt type mixing of `template` with `system/user/assistant` detected.')

            elif 'when' in _p:
                self._validate(_p['prompt'])

            elif 'loop' in _p:
                self._validate(_p['prompt'])

            elif 'switch' in _p:
                for case in _p['prompt']:
                    self._validate(_p['prompt'][case])

            else:
                raise Exception(f'Invalid prompt type {_p}')
