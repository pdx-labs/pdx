import json
from time import time
from pdx.logger import logger
from pdx.models.model import Model
from pdx.prompt.prompt_session import PromptSession
from pdx.models.elevenlabs.client import ElevenLabsClient
from pdx.models.metadata import ModelResponse, ResponseMetadata


class TextToSpeechModel(Model):
    def __init__(self,
                 api_key: str,
                 **kwargs,
                 ):

        self._provider = "elevenlabs"
        self._client = ElevenLabsClient(api_key)
        # Currently: eleven_monolingual_v1, eleven_multilingual_v1
        self._model = kwargs.get('model', 'eleven_multilingual_v1')
        # https://api.elevenlabs.io/v1/voices
        self._voice_id = kwargs.get('voice_id', '21m00Tcm4TlvDq8ikWAM')
        # 0, 1, 2, 3, 4
        self._optimize_streaming_latency = kwargs.get(
            'optimize_streaming_latency', 0)
        self._api_url = f"/v1/text-to-speech/{self._voice_id}?optimize_streaming_latency={self._optimize_streaming_latency}"
        # Voice settings overriding stored setttings for the given voice.
        # They are applied only on the given TTS request.
        self._stability = kwargs.get('stability', 0.5)
        self._similarity_boost = kwargs.get('similarity_boost', 0.5)

        self._retries = kwargs.get('retries', 2)

    def _preprocess(self, prompt: PromptSession) -> dict:
        _prompt = prompt.text_prompt({})

        request_params = {
            "model": self._model,
            "text": _prompt,
            "voice_settings": {
                "stability": self._stability,
                "similarity_boost": self._similarity_boost
            }
        }

        return request_params

    def _postprocess(self, response: dict, request_params: dict, request_time: float) -> ModelResponse:
        _prompt = request_params.pop('text', None)

        request_params['voice_id'] = self._voice_id
        request_params['optimize_streaming_latency'] = self._optimize_streaming_latency

        response_metadata = ResponseMetadata(
            model=request_params['model'],
            stop='tts_completed',
            stop_reason='tts_completed',
            latency=request_time)

        _data_type = f'audio_bytes'

        model_response = ModelResponse(
            metadata=response_metadata,
            request_params=request_params,
            data=response,
            data_type=_data_type
        )

        return model_response
