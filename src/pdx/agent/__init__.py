from typing import Union
from uuid import uuid4
from pdx.prompt import Prompt
from pdx.models.model import Model
from pdx.prompt.prompt_chain import PromptChain
from pdx.prompt.prompt_tree import PromptTree
from pdx.prompt.prompt_session import PromptSession
from pdx.models.metadata import ModelResponse
from pdx.agent.metadata import AgentID, RequestMetadata, AgentResponse, AgentResponseMetadata


class Agent(object):
    def __init__(self, prompt: Union[Prompt, PromptChain, PromptTree], model: Model):

        self._prompt = prompt
        self._model = model
        self._agent_id = AgentID(agent_name='agent_name')

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
        worker_response = AgentResponse(
            data=response.completion,
            metadata=metadata
        )
        return worker_response

    async def aexecute(self, request: dict = {}, metadata: dict = {}):
        _prompt_session = self._prompt.execute(request)
        _model_response = await self._model.aexecute(_prompt_session)
        _worker_response = self._postprocess(
            _model_response, request, _prompt_session)
        _worker_response.metadata.add_custom(metadata=metadata)
        return _worker_response

    def execute(self, request: dict = {}, metadata: dict = {}):
        _prompt_session = PromptSession()
        _prompt_session = self._prompt.execute(request)
        _model_response = self._model.execute(_prompt_session)
        _worker_response = self._postprocess(
            _model_response, request, _prompt_session)
        _worker_response.metadata.add_custom(metadata=metadata)
        return _worker_response


# from typing import List, Dict, Union
# from pdx.logger import logger
# from pdx.settings import Keys
# from pdx.prompt.prompt_tree import PromptTree, PromptChain
# from pdx.agent.config import AgentConfig
# from pdx.agent.metadata import AgentID, AgentResponse


# Request = Union[str, int, float, Dict, List]

# class AgentBuilder:
#     def __init__(self, path: str = None, config_path: str = None):
#         self._folder_path = path
#         self._config: AgentConfig = AgentConfig(path)
#         self.prompt_tree: PromptTree = PromptTree(self._config.prompt_config)
#         self._completion_agent = CompletionAgent(
#             self._config.model_config, self._api_keys)

#         self._agent_id = AgentID(agent_name=self._config.name)

#     async def aexecute(self, request: dict = {}, metadata: dict = {}) -> AgentResponse:
#         _prompt = PromptChain(self._config.prompt_config.prompt_type)
#         self.prompt_tree.execute(request, _prompt)
#         _response = await self._completion_agent.aexecute(_prompt, request, self._agent_id)
#         _response.metadata.add_custom(metadata=metadata)
#         return _response

#     def execute(self, request: dict, metadata: dict = {}) -> AgentResponse:
#         _prompt = PromptChain(self._config.prompt_config.prompt_type)
#         self.prompt_tree.execute(request, _prompt)
#         _response = self._completion_agent.execute(
#             _prompt, request, self._agent_id)
#         _response.metadata.add_custom(metadata=metadata)
#         return _response
