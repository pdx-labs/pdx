from dataclasses import dataclass, field

# Available LLM completion models
OPENAI_MODELS = ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"]
ANTHROPIC_MODELS = ["claude-v1", "claude-v1-100k", "claude-instant-v1", "claude-instant-v1-100k",
                    "claude-v1.3", "claude-v1.3-100k", "claude-v1.2" "claude-v1.0", "claude-instant-v1.1",
                    "claude-instant-v1.1-100k", "claude-instant-v1.0"]


@dataclass
class ModelConfig:
    id: str
    provider: str = field(init=False)
    api_key_id: str = field(init=False)

    def __post_init__(self):
        if self.id in [*OPENAI_MODELS]:
            self.api_key_id = 'openai_key'
            self.provider = 'openai'
        elif self.id in [*ANTHROPIC_MODELS]:
            self.api_key_id = 'anthropic_key'
            self.provider = 'anthropic'
        else:
            raise ValueError(f"Model: {self.id} not supported")


def model_builder(self,
                  api_key: str,
                  model: str,
                  **kwargs,
                  ):
    if model in OPENAI_MODELS:
        self._provider = "openai"
        # self._client = OpenAI(api_key, model, max_tokens,
        #                       stop, temperature, **kwargs)
    elif model in ANTHROPIC_MODELS:
        self._provider = "anthropic"
        # self._client = Anthropic(api_key, model, max_tokens,
        #                          stop, temperature, **kwargs)
    else:
        raise Exception("Model not supported")
