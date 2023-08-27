import json
from time import time
from pdx.logger import logger
from pdx.models.model import Model
from pdx.prompt.prompt_session import PromptSession
from pdx.models.replicate.client import ReplicateClient
from pdx.models.metadata import ModelResponse, ResponseMetadata
from pprint import pprint


class PredictionModel(Model):
    def __init__(self,
                 api_key: str,
                 model: str,
                 retries: int = 2,
                 poll_interval: int = 7,
                 **kwargs,
                 ):

        self._provider = "replicate"
        self._client = ReplicateClient(api_key, poll_interval=poll_interval)

        self._api_url = f"v1/predictions"
        self._model = model

        if kwargs:
            self._model_params = kwargs
        else:
            self._model_params = {}

        self._retries = retries

    def _preprocess(self, prompt: PromptSession) -> dict:
        _prompt = prompt.text_prompt({})

        _input = self._model_params
        _input['prompt'] = _prompt

        request_params = {
            "version": self._model,
            "input": _input
        }

        return request_params

    def _postprocess(self, response: dict, request_params: dict, request_time: float) -> ModelResponse:

        _r = json.loads(response)

        _input_params = request_params.pop('input', None)
        _prompt = _input_params.pop('prompt', None)
        _input_model_id = request_params.pop('version', None)

        _other = {
            'metrics': _r['metrics'],
            'created_at': _r['created_at'],
            'started_at': _r['started_at'],
            'completed_at': _r['completed_at'],
        }
        response_metadata = ResponseMetadata(
            model=_r['version'],
            api_log_id=_r['id'],
            stop=_r['status'],
            stop_reason=_r['status'],
            warnings=_r['error'],
            other=_other,
            latency=request_time)

        _data_type = f'text_object'

        model_response = ModelResponse(
            metadata=response_metadata,
            request_params=_input_params,
            data=_r['output'],
            data_type=_data_type
        )

        return model_response
