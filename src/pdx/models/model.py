from time import time
from pdx.logger import logger
from pdx.prompt.prompt_session import PromptSession
from pdx.models.api_client import APIClient
from pdx.models.metadata import ModelResponse, ResponseMetadata, ModelTokenUsage


class Model:
    def __init__(self,
                 api_key: str,
                 model: str,
                 max_tokens: int = 1200,
                 stop: list = ["#", "---"],
                 temperature: float = 0,
                 **kwargs
                 ):

        self._client = APIClient(api_key)
        self._provider = "model_provider"
        self._model = model
        self._max_tokens = max_tokens
        self._stop = stop
        self._temperature = temperature
        self._retries = kwargs.get('retries', 2)

        self._api_url = "v1/completions"

    def _preprocess(self, prompt: PromptSession) -> dict:
        request_params = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
            "stop": self._stop
        }

        _prompt = prompt.text_prompt({})

        request_params['prompt'] = _prompt

        return request_params

    def _postprocess(self, response: dict, request_params: dict, request_time: float) -> ModelResponse:
        token_usage = ModelTokenUsage(
            response=response['usage']['completion_tokens'],
            prompt=response['usage']['prompt_tokens'],
            total=response['usage']['total_tokens']
        )
        response_metadata = ResponseMetadata(
            model=response['model'],
            api_log_id=response['id'],
            stop=response['choices'][0]['finish_reason'],
            stop_reason=response['choices'][0]['finish_reason'],
            token_usage=token_usage,
            latency=request_time)

        params = {key: value for key,
                  value in request_params.items() if key != 'prompt'}
        model_response = ModelResponse(
            metadata=response_metadata,
            request_params=params,
            data=response['choices'][0]['text'])
        return model_response

    def execute(self, prompt: PromptSession) -> ModelResponse:
        start_time = time()
        request_params = self._preprocess(prompt)

        _try_count = 0
        while (_try_count <= self._retries):
            try:
                _r = self._client.request(
                    "post",
                    self._api_url,
                    params=request_params,
                )
                request_time = time() - start_time
                return self._postprocess(_r, request_params, request_time)
            except Exception as e:
                logger.verbose(
                    f"{self._provider} {self._model} model failed to run.\nReason: {e}")
                _try_count += 1

        raise ValueError(
            f"{self._provider} {self._model} model failed to run successfully.")

    async def aexecute(self, prompt: PromptSession) -> ModelResponse:
        start_time = time()
        request_params = self._preprocess(prompt)

        _try_count = 0
        while (_try_count <= self._retries):
            try:
                _r = await self._client.arequest(
                    "post",
                    self._api_url,
                    params=request_params,
                )
                request_time = time() - start_time
                return self._postprocess(_r, request_params, request_time)
            except Exception as e:
                logger.verbose(
                    f"{self._provider} {self._model} model failed to run.\nReason: {e}")
                _try_count += 1

        raise ValueError(
            f"{self._provider} {self._model} model failed to run successfully.")
