from pdx.logger import logger
from pdx.agent.prompt_session import PromptSession
from pdx.models.openai.client import OpenAIClient
from pdx.models.metadata import ModelResponse, ResponseMetadata, ModelTokenUsage
from time import time


class OpenAI(object):
    def __init__(self,
                 api_key: str,
                 model: str,
                 max_tokens: int = 1200,
                 stop: list = ["#", "---"],
                 temperature: float = 0,
                 **kwargs,
                 ):
        if model in ["gpt-3.5-turbo", "gpt-4"]:
            self._client_type = "chat"
        elif model in ["text-davinci-003", "text-davinci-002", "davinci", "curie", "babbage", "ada"]:
            self._client_type = "text"
        else:
            raise Exception("Model not supported")

        self._provider = "openai"
        self._client = OpenAIClient(api_key)
        self._model = model
        self._max_tokens = max_tokens
        self._stop = stop
        self._temperature = temperature
        self._top_p = kwargs.get('top_p', 1)
        self._best_of = kwargs.get('best_of', 1)
        self._frequency_penalty = kwargs.get('frequency_penalty', 0)
        self._presence_penalty = kwargs.get('presence_penalty', 0)

    def _preprocess(self, prompt: PromptSession):
        request_params = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "temperature": self._temperature,
            "top_p": self._top_p,
            "frequency_penalty": self._frequency_penalty,
            "presence_penalty": self._presence_penalty,
            "stop": self._stop
        }
        if self._client_type == "chat":
            if prompt.type == "text":
                _prompt_session = prompt.text_to_chat_prompt_openai()
            else:
                _prompt_session = prompt.session
            request_params['messages'] = _prompt_session

        if self._client_type == "text":
            if prompt.type == "chat":
                _prompt_session = prompt.chat_to_text_prompt_openai()
            else:
                _prompt_session = prompt.stitch_for_text_completion()
            request_params['prompt'] = _prompt_session
            request_params['best_of'] = self._best_of

        return request_params

    def _postprocess(self, response: dict, request_params: dict, completion_time: float) -> ModelResponse:
        token_usage = ModelTokenUsage(
            completion=response['usage']['completion_tokens'],
            prompt=response['usage']['prompt_tokens'],
            total=response['usage']['total_tokens'])
        response_metadata = ResponseMetadata(
            model=response['model'],
            api_log_id=response['id'],
            stop=response['choices'][0]['finish_reason'],
            stop_reason=response['choices'][0]['finish_reason'],
            token_usage=token_usage,
            completion_time=completion_time)

        if self._client_type == "chat":
            params = {key: value for key,
                      value in request_params.items() if key != 'messages'}
            model_response = ModelResponse(
                metadata=response_metadata,
                request_params=params,
                completion=response['choices'][0]['message']['content'])
            return model_response

        if self._client_type == "text":
            params = {key: value for key,
                      value in request_params.items() if key != 'prompt'}
            model_response = ModelResponse(
                metadata=response_metadata,
                request_params=params,
                completion=response['choices'][0]['text'])
            return model_response

    def run(self, prompt: PromptSession) -> ModelResponse:
        start_time = time()
        request_params = self._preprocess(prompt)
        if self._client_type == "chat":
            _r = self._client.completion_chat(**request_params)
        if self._client_type == "text":
            _r = self._client.completion(**request_params)
        completion_time = time() - start_time
        return self._postprocess(_r, request_params, completion_time)

    async def arun(self, prompt: PromptSession) -> ModelResponse:
        start_time = time()
        request_params = self._preprocess(prompt)
        if self._client_type == "chat":
            _r = await self._client.acompletion_chat(**request_params)
        if self._client_type == "text":
            _r = await self._client.acompletion(**request_params)
        completion_time = time() - start_time
        return self._postprocess(_r, request_params, completion_time)
