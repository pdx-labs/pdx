from time import time
from pdx.logger import logger
from pdx.models.model import Model
from pdx.prompt.prompt_session import PromptSession
from pdx.models.openai.client import OpenAIClient
from pdx.models.metadata import ModelResponse, ResponseMetadata, ModelTokenUsage


class CompletionModel(Model):
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

        if self._client_type == "chat":
            self._api_url = "v1/chat/completions"
        else:  # self._client_type == "text"
            self._api_url = "v1/completions"

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
        self._retries = kwargs.get('retries', 2)

    def _preprocess(self, prompt: PromptSession) -> dict:
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
            if prompt.session_type == "text":
                _content = prompt.text_prompt({})
                _chat_prompt = [{"role": "user", "content": _content}]
            else:
                _chat_prompt = prompt.chat_prompt()
            request_params['messages'] = _chat_prompt

        if self._client_type == "text":
            if prompt.session_type == "chat":
                _text_prompt = prompt.text_prompt()
            else:
                _text_prompt = prompt.text_prompt({})
            request_params['prompt'] = _text_prompt
            request_params['best_of'] = self._best_of

        return request_params

    def _postprocess(self, response: dict, request_params: dict, request_time: float) -> ModelResponse:
        token_usage = ModelTokenUsage(
            response=response['usage']['completion_tokens'],
            prompt=response['usage']['prompt_tokens'],
            total=response['usage']['total_tokens'])
        response_metadata = ResponseMetadata(
            model=response['model'],
            api_log_id=response['id'],
            stop=response['choices'][0]['finish_reason'],
            stop_reason=response['choices'][0]['finish_reason'],
            token_usage=token_usage,
            latency=request_time)

        if self._client_type == "chat":
            params = {key: value for key,
                      value in request_params.items() if key != 'messages'}
            model_response = ModelResponse(
                metadata=response_metadata,
                request_params=params,
                data=response['choices'][0]['message']['content'])
            return model_response

        if self._client_type == "text":
            params = {key: value for key,
                      value in request_params.items() if key != 'prompt'}
            model_response = ModelResponse(
                metadata=response_metadata,
                request_params=params,
                data=response['choices'][0]['text'])
            return model_response
