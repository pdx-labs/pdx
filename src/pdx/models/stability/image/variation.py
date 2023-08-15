import json
import base64
from pdx.logger import logger
from pdx.models.model import Model
from pdx.prompt.prompt_session import PromptSession
from pdx.models.stability.client import StabilityClient
from pdx.models.metadata import ModelResponse, ResponseMetadata
from pdx.models.utils.image import format_response


class ImageVariationModel(Model):
    def __init__(self,
                 api_key: str,
                 **kwargs,
                 ):

        self._provider = "stability"
        self._client = StabilityClient(api_key)
        self._engine_id = kwargs.get(
            'engine_id', 'stable-diffusion-v1-5')
        self._model = kwargs.get(
            'engine_id', 'stable-diffusion-v1-5')
        self._api_url = f"v1/generation/{self._engine_id}/image-to-image"

        # STEP_SCHEDULE, IMAGE_STRENGTH
        self._init_image_mode = kwargs.get('init_image_mode', 'IMAGE_STRENGTH')
        # image_strength float [ 0.0, 1.0 ]
        self._image_strength = kwargs.get('init_image_strength', 0.35)
        # step_schedule_start float [ 0.0, 1.0 ] also 1 - image_strength
        self._step_schedule_start = kwargs.get('step_schedule_start', 0.65)
        # step_schedule_end float [ 0.0, 1.0 ] to skip the end portion of the diffusion step
        self._step_schedule_end = kwargs.get('step_schedule_end', None)
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
            'init_image_mode': self._init_image_mode,
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

        if self._init_image_mode == 'IMAGE_STRENGTH':
            request_params['image_strength'] = self._image_strength
        elif self._init_image_mode == 'STEP_SCHEDULE':
            request_params['step_schedule_start'] = self._step_schedule_start
            if self._step_schedule_end is not None:
                request_params['step_schedule_end'] = self._step_schedule_end
        else:
            pass

        _prompts = prompt.chat_prompt(with_metadata=True)
        for idx, _p in enumerate(_prompts):
            request_params[f'text_prompts[{idx}][text]'] = _p['content']
            request_params[f'text_prompts[{idx}][weight]'] = _p.get(
                'weight', 1)

        _images: list = prompt.image_prompt()
        if len(_images) > 1:
            logger.echo('Only one image prompt supported at the moment.')
        request_params['files'] = {
            "init_image": (_images[0][0], _images[0][1])}

        return request_params

    def _postprocess(self, response: dict, request_params: dict, request_time: float) -> ModelResponse:
        _prompt_keys = [x for x in request_params.keys()
                        if 'text_prompts' in x]
        print(_prompt_keys)
        for _k in _prompt_keys:
            _ = request_params.pop(_k, None)
        request_params.pop('text_prompts', None)
        _files = request_params.pop('files', None)
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
