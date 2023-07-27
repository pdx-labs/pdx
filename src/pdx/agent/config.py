import os
from pdx.utils.rw import read_yaml
from pdx.models.config import ModelConfig
from pdx.prompt.config import PromptConfig


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

        model_params = {key: value for key,
                        value in _config_dict['model'].items() if key not in ['id']}
        self.model_config = ModelConfig(
            id=_config_dict['model']['id'], params=model_params)
        self.prompt_config = PromptConfig(
            _config_dict['prompt'], templates_path)
