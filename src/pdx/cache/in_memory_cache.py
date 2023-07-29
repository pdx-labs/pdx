from pdx.cache.cache import Cache
from pdx.cache.utils import _hash_request_values
from pdx.agent.metadata import AgentResponse, AgentID, AgentRequest


class InMemoryCache(Cache):

    def __init__(self) -> None:
        self._cache = {}

    def lookup(self, agent_id: AgentID, agent_request_values: AgentRequest) -> str:
        _hash_string = _hash_request_values(agent_request_values)
        return self._cache.get((agent_id.unique_id, _hash_string), None)

    def update(self, agent_id: AgentID, agent_request_values: AgentRequest, agent_response: AgentResponse) -> None:
        _hash_string = _hash_request_values(agent_request_values)
        self._cache[(agent_id.unique_id, _hash_string)] = agent_response

    def clear(self) -> None:
        self._cache = {}
