from dataclasses import dataclass, field
from pdx.models.openai import OpenAI
from pdx.models.anthropic import Anthropic
from pdx.agent.prompt_session import PromptSession
from pdx.models.metadata import ModelResponse

# Available LLM completion models
OPENAI_MODELS = ["text-davinci-003", "gpt-3.5-turbo", "gpt-4"]
ANTHROPIC_MODELS = ["claude-v1", "claude-v1-100k", "claude-instant-v1", "claude-instant-v1-100k",
                    "claude-v1.3", "claude-v1.3-100k", "claude-v1.2" "claude-v1.0", "claude-instant-v1.1",
                    "claude-instant-v1.1-100k", "claude-instant-v1.0"]


@dataclass
class ModelConfig:
    id: str
    key_id: str = field(init=False)

    def __post_init__(self):
        if self.id in [*OPENAI_MODELS]:
            self.key_id = 'openai_key'
        elif self.id in [*ANTHROPIC_MODELS]:
            self.key_id = 'anthropic_key'
        else:
            raise ValueError(f"Model: {self.id} not supported")


class CompletionModel(object):
    def __init__(self,
                 api_key: str,
                 model: str,
                 max_tokens: int = 1200,
                 stop: list = ["#", "---"],
                 temperature: float = 0,
                 **kwargs,
                 ):
        if model in OPENAI_MODELS:
            self._provider = "openai"
            self._client = OpenAI(api_key, model, max_tokens,
                                  stop, temperature, **kwargs)
        elif model in ANTHROPIC_MODELS:
            self._provider = "anthropic"
            self._client = Anthropic(api_key, model, max_tokens,
                                     stop, temperature, **kwargs)
        else:
            raise Exception("Model not supported")

        self._retries = 2

    def run(self, prompt: PromptSession) -> ModelResponse:
        return self._client.run(prompt)

    async def arun(self, prompt: PromptSession) -> ModelResponse:
        return await self._client.arun(prompt)
