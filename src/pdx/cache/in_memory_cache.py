from pdx.cache.cache import Cache
from pdx.cache.utils import _hash_request_values
from pdx.agent.metadata import AgentResponse, AgentID, AgentRequest


class InMemoryCache(Cache):

    def __init__(self) -> None:
        self._cache = {}

    def lookup(self, agent_id: AgentID, agent_request: AgentRequest) -> str:
        _hash_string = _hash_request_values(agent_request)
        _cached_response = self._cache.get(
            (agent_id.unique_id, _hash_string), None)
        if _cached_response:
            _agent_response = AgentResponse(**_cached_response)
            return _agent_response
        else:
            return None

    def update(self, agent_id: AgentID, agent_request: AgentRequest, agent_response: AgentResponse) -> None:
        _hash_string = _hash_request_values(agent_request)
        self._cache[(agent_id.unique_id, _hash_string)
                    ] = agent_response.model_dump(mode='json')

    def clear(self) -> None:
        self._cache = {}

    def evict(self) -> None:
        self._cache = {}
