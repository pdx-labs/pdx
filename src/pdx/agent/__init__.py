from typing import List, Dict, Union
from pdx.logger import logger
from pdx.settings import Keys
from pdx.agent.completer import CompletionAgent
from pdx.agent.prompt import PromptTree, PromptSession
from pdx.agent.config import AgentConfig
from pdx.agent.metadata import AgentID
from dataclasses import asdict

Request = Union[str, int, float, Dict, List]


class AgentBuilder:
    def __init__(self, folder_path: str, api_keys: Keys = None):
        self._folder_path = folder_path
        if api_keys is None:
            self._api_keys = Keys()
        else:
            self._api_keys = api_keys
        self._config: AgentConfig = AgentConfig(folder_path)
        self.prompt_tree: PromptTree = PromptTree(self._config.prompt_config)
        self._completion_agent = CompletionAgent(
            self._config.model_config, self._api_keys)

        self._agent_id = AgentID(agent_name=self._config.name)

    async def aexecute(self, request: dict, agent_response: bool = False):
        _prompt = PromptSession(self._config.prompt_config.prompt_type)
        self.prompt_tree.execute(request, _prompt)
        response = await self._completion_agent.aexecute(_prompt, self._agent_id)
        logger.debug(asdict(response))
        return response.completion

    def execute(self, request: dict, agent_response: bool = False):
        _prompt = PromptSession(self._config.prompt_config.prompt_type)
        self.prompt_tree.execute(request, _prompt)
        response = self._completion_agent.execute(_prompt, self._agent_id)
        logger.debug(asdict(response))
        return response.completion
