import os
from pdx.utils.rw import read_yaml
from pdx.models import ModelConfig


class AgentConfig:
    def __init__(self, folder_path: str):
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            config_path = os.path.join(folder_path, "config.yaml")
            if os.path.exists(config_path):
                _config_dict = read_yaml(config_path)
            else:
                raise ValueError(f"Config file not found in {folder_path}")

            if 'name' in _config_dict:
                self.name = _config_dict['name']
            else:
                self.name = os.path.basename(folder_path)
        else:
            raise ValueError(
                f"Agent path not found or not a directory: {folder_path}")

        templates_path = os.path.join(folder_path, "templates")
        if not os.path.exists(templates_path):
            raise ValueError(f"Templates folder not found in {folder_path}")

        self.model_config = ModelConfig(**_config_dict['model'])
        self.prompt_config = PromptConfig(
            _config_dict['prompt'], templates_path)


class PromptConfig:
    def __init__(self, config: dict, templates_path: str):
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
                self.validate(_p['prompt'])

            elif 'loop' in _p:
                self.validate(_p['prompt'])

            elif 'switch' in _p:
                for case in _p['prompt']:
                    self.validate(_p['prompt'][case])

            else:
                raise Exception(f'Invalid prompt type {_p}')
