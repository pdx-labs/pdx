from pydantic import BaseSettings
from dataclasses import dataclass, field

# Available LLM completion models
OPENAI_COMPLETION_MODELS = ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"]
ANTHROPIC_COMPLETION_MODELS = ["claude-v1", "claude-v1-100k", "claude-instant-v1", "claude-instant-v1-100k",
                               "claude-v1.3", "claude-v1.3-100k", "claude-v1.2" "claude-v1.0", "claude-instant-v1.1",
                               "claude-instant-v1.1-100k", "claude-instant-v1.0"]


class Keys(BaseSettings):
    openai_key: str = None
    anthropic_key: str = None
    cohere_key: str = None


@dataclass
class ModelConfig:
    id: str
    params: dict = field(default_factory=dict)
    name: str = field(init=False)
    provider: str = field(init=False)
    api_key: str = field(init=False)

    def __post_init__(self):
        self.name = self.id

        if self.id in [*OPENAI_COMPLETION_MODELS]:
            api_key_id = 'openai_key'
            self.provider = 'openai'
        elif self.id in [*ANTHROPIC_COMPLETION_MODELS]:
            api_key_id = 'anthropic_key'
            self.provider = 'anthropic'
        else:
            raise ValueError(f"Model: {self.id} not supported")

        self.api_key = self._get_api_key(api_key_id)

    @staticmethod
    def _get_api_key(api_key_id: str):
        _keys = Keys()
        _api_key = _keys.__dict__.get(api_key_id, None)

        if _api_key is None:
            raise ValueError(
                f"{api_key_id.capitalize()} API key not found. Make sure it is present as a environment variable.")

        return _api_key

    def build_model(self):
        if self.id in [*OPENAI_COMPLETION_MODELS]:
            from pdx.models.openai import CompletionModel as OpenAICompletionModel
            return OpenAICompletionModel(model=self.id, api_key=self.api_key, **self.params)
        elif self.id in [*ANTHROPIC_COMPLETION_MODELS]:
            from pdx.models.anthropic import CompletionModel as AnthropicCompletionModel
            return AnthropicCompletionModel(model=self.id, api_key=self.api_key, **self.params)
        else:
            raise ValueError(f"Model: {self.id} not supported")
