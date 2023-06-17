from pdx.logger import logger
from pdx.agent.prompt_session import PromptSession
from pdx.models.anthropic.client import AnthropicClient
from pdx.models.anthropic.exceptions import handle_anthropic_prompt_validation
from pdx.models.metadata import ModelResponse, ResponseMetadata, ModelTokenUsage
from time import time


class Anthropic(object):
    def __init__(self,
                 api_key: str,
                 model: str,
                 max_tokens: int = 1200,
                 stop: list = ["#", "---"],
                 temperature: float = 0,
                 **kwargs,
                 ):

        self._provider = "anthropic"
        self._client = AnthropicClient(api_key)
        self._model = model
        self._max_tokens_to_sample = max_tokens
        self._stop_sequences = stop
        self._temperature = temperature
        self._top_p = kwargs.get('top_p', -1)
        self._top_k = kwargs.get('top_k', -1)

    def _preprocess(self, prompt: PromptSession):
        _prompt_session = prompt.session_to_prompt_anthropic()
        handle_anthropic_prompt_validation(_prompt_session)
        request_params = {
            'prompt': _prompt_session,
            'stop_sequences': self._stop_sequences,
            'model': self._model,
            'max_tokens_to_sample': self._max_tokens_to_sample,
            'temperature': self._temperature,
            'top_p': self._top_p,
            'top_k': self._top_k,
        }

        logger.debug(_prompt_session)

        return request_params

    def _postprocess(self, response: dict, request_params: dict, completion_time) -> ModelResponse:
        params = {key: value for key,
                  value in request_params.items() if key != 'prompt'}
        token_usage = ModelTokenUsage(
            completion=None,
            prompt=None,
            total=None)
        response_metadata = ResponseMetadata(
            model=response['model'],
            api_log_id=response['log_id'],
            stop=response['stop'],
            stop_reason=response['stop'],
            token_usage=token_usage,
            completion_time=completion_time)
        model_response = ModelResponse(
            metadata=response_metadata,
            request_params=params,
            completion=response['completion'])

        return model_response

    def run(self, prompt: PromptSession) -> ModelResponse:
        start_time = time()
        request_params = self._preprocess(prompt)
        _r = self._client.completion(**request_params)
        completion_time = time() - start_time
        return self._postprocess(_r, request_params, completion_time)

    async def arun(self, prompt: PromptSession) -> ModelResponse:
        start_time = time()
        request_params = self._preprocess(prompt)
        _r = await self._client.acompletion(**request_params)
        completion_time = time() - start_time
        return self._postprocess(_r, request_params, completion_time)
