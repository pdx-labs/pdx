from abc import ABC, abstractmethod
from pdx.agent.metadata import AgentResponse, AgentID, AgentRequest


class Cache(ABC):
    """Cache abstract base class for caching Agent requests."""

    @abstractmethod
    def lookup(self, agent_id: AgentID, agent_request: AgentRequest):
        """Cache lookup."""

    @abstractmethod
    def update(self, agent_id: AgentID, agent_request: AgentRequest, agent_response: AgentResponse):
        """Update cache."""

    @abstractmethod
    def evict(self, **kwargs):
        """Evict cache."""

    @abstractmethod
    def clear(self, **kwargs):
        """Clear cache."""
