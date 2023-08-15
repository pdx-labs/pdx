import json
import base64
from pdx.logger import logger
from pdx.models.model import Model
from pdx.prompt.prompt_session import PromptSession
from pdx.models.stability.client import StabilityClient
from pdx.models.metadata import ModelResponse, ResponseMetadata


class ImageGenerationModel(Model):
    def __init__(self,
                 api_key: str,
                 **kwargs,
                 ):

        self._provider = "stability"
        self._client = StabilityClient(api_key)
        self._engine_id = kwargs.get(
            'engine_id', 'stable-diffusion-xl-1024-v1-0')
        self._model = kwargs.get(
            'engine_id', 'stable-diffusion-xl-1024-v1-0')
        self._api_url = f"v1/generation/{self._engine_id}/text-to-image"

        # DiffuseImageHeight int multiple of 64 >= 128
        self._height = kwargs.get('height', 1024)
        # DiffuseImageWidth int multiple of 64 >= 128
        self._width = kwargs.get('width', 1024)
        # cfg_scale int  [0, 35]
        self._cfg_scale = kwargs.get('cfg_scale', 7)
        # clip_guidance_preset	str [FAST_BLUE FAST_GREEN NONE SIMPLE SLOW SLOWER SLOWEST]
        self._clip_guidance_preset = kwargs.get('clip_guidance_preset', 'NONE')
        # sampler str [DDIM DDPM K_DPMPP_2M K_DPMPP_2S_ANCESTRAL K_DPM_2 K_DPM_2_ANCESTRAL K_EULER K_EULER_ANCESTRAL K_HEUN K_LMS]
        self._sampler = kwargs.get('sampler', None)
        # samples int [1, 10]
        self._samples = kwargs.get('samples', 1)
        # seed int [0, 2**32] 4294967295
        self._seed = kwargs.get('seed', 0)
        # steps int [ 10 .. 150 ]
        self._steps = kwargs.get('steps', 50)
        # style_preset str [3d-model analog-film anime cinematic comic-book digital-art enhance fantasy-art isometric line-art low-poly modeling-compound neon-punk origami photographic pixel-art tile-texture]
        self._style_preset = kwargs.get('style_preset', None)

        # activate or deactivate the decoding of str to bytes
        self._decode_response = kwargs.get('decode_response', True)
        self._retries = kwargs.get('retries', 2)

    def _preprocess(self, prompt: PromptSession) -> dict:
        request_params = {
            'height': self._height,
            'width': self._width,
            'cfg_scale': self._cfg_scale,
            'clip_guidance_preset': self._clip_guidance_preset,
            'samples': self._samples,
            'seed': self._seed,
            'steps': self._steps,
        }
        if self._sampler is not None:
            request_params['sampler'] = self._sampler
        if self._style_preset is not None:
            request_params['style_preset'] = self._style_preset

        _prompts = prompt.chat_prompt(with_metadata=True)
        _text_prompts = []
        for _p in _prompts:
            _text_prompts.append({
                'text': _p['content'],
                'weight': _p.get('weight', 1)
            })

        request_params['text_prompts'] = _text_prompts

        return request_params

    def _postprocess(self, response: dict, request_params: dict, request_time: float) -> ModelResponse:
        # _prompt = request_params.pop('text_prompts', None)
        _r: dict = json.loads(response)

        _seed = None
        _artifacts = _r.get('artifacts', [])

        if len(_artifacts) == 0:
            _data = None
        elif len(_artifacts) == 1:
            _data = base64.b64decode(_artifacts[0]['base64'])
            _seed = _artifacts[0]['seed']
        elif len(_artifacts) > 1:
            _data = []
            _seed = []
            for _a in _artifacts:
                _data.append(base64.b64decode(_a['base64']))
                _seed.append(_a['seed'])

        _data_type_suffix = ''
        if isinstance(_data, list):
            _data_type_suffix = '_list'

        _data_type = f'image_bytes{_data_type_suffix}'

        response_metadata = ResponseMetadata(
            model=self._model,
            stop='success',
            stop_reason='success',
            latency=request_time,
            other={'seed': _seed})

        model_response = ModelResponse(
            metadata=response_metadata,
            request_params=request_params,
            data=_data,
            data_type=_data_type
        )

        return model_response
