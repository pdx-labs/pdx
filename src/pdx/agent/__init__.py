from typing import Union
from uuid import uuid4
from pdx.agent.config import AgentConfig
from pdx.prompt import Prompt
from pdx.models.model import Model
from pdx.prompt.prompt_chain import PromptChain
from pdx.prompt.prompt_tree import PromptTree
from pdx.prompt.prompt_session import PromptSession
from pdx.models.metadata import ModelResponse
from pdx.agent.metadata import AgentID, RequestMetadata, AgentResponse, AgentResponseMetadata, AgentRequest
from pdx.cache.cache import Cache
from pdx.cache import agent_cache, aagent_cache


class Agent(object):
    def __init__(self, path: str = None, prompt: Union[Prompt, PromptChain, PromptTree] = None, model: Model = None, cache: Cache = None):
        if path is not None:
            self._type = 'config'
            self._config: AgentConfig = AgentConfig(path)
            self._agent_id = AgentID(agent_name=self._config.name)
            if prompt is None:
                self._prompt: PromptTree = PromptTree(
                    self._config.prompt_config)
            else:
                self._prompt = prompt

            if model is None:
                self._model: Model = self._config.model_config.build_model()
            else:
                self._model = model
        else:
            if prompt is None and model is None:
                raise ValueError(
                    'Provide `Prompt` and `Model` if not providing Agent config path.')
            self._type = 'prompt-model'
            self._prompt = prompt
            self._model = model
            self._agent_id = AgentID()

        self._cache = cache

    def _postprocess(self, response: ModelResponse, request: dict, prompt_session: PromptSession) -> AgentResponse:
        request_metadata = RequestMetadata(
            agent_id=self._agent_id,
            request_id=uuid4(),
            request_values=request,
            request_params=response.request_params,
            prompt=prompt_session.export()
        )
        metadata = AgentResponseMetadata(
            request=request_metadata,
            response=response.metadata
        )
        agent_response = AgentResponse(
            data=response.data,
            metadata=metadata
        )
        return agent_response

    @aagent_cache
    async def aexecute(self, request: AgentRequest = {}, metadata: dict = {}):
        _prompt_session = self._prompt.execute(request)
        _model_response = await self._model.aexecute(_prompt_session)
        _agent_response = self._postprocess(
            _model_response, request, _prompt_session)
        _agent_response.metadata.add_custom(metadata=metadata)
        return _agent_response

    @agent_cache
    def execute(self, request: AgentRequest = {}, metadata: dict = {}):
        _prompt_session = self._prompt.execute(request)
        _model_response = self._model.execute(_prompt_session)
        _agent_response = self._postprocess(
            _model_response, request, _prompt_session)
        _agent_response.metadata.add_custom(metadata=metadata)
        return _agent_response
