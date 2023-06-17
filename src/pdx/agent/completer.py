from pdx.models import CompletionModel, ModelConfig
from pdx.settings import Keys
from pdx.agent.prompt_session import PromptSession
from pdx.agent.metadata import AgentID, AgentRequest
from pdx.logger import logger
from uuid import uuid4


class CompletionAgent(object):
    def __init__(self, model: ModelConfig, api_keys: Keys):
        _api_key = api_keys.__dict__.get(model.key_id, None)

        if _api_key is None:
            raise ValueError(
                f"{model.key_id.capitalize()} API key not found")

        self._model = CompletionModel(_api_key, model=model.id)
        self._retries = 2

    def execute(self, prompt: PromptSession, agent_id: AgentID = None) -> AgentRequest:
        try_count = 0
        while (try_count <= self._retries):
            try:
                _r = self._model.run(prompt)
                agent_request = AgentRequest(
                    agent_id=agent_id,
                    request_id=uuid4(),
                    request_params=_r.request_params,
                    prompt=prompt.session,
                    completion=_r.completion,
                    metadata=_r.metadata)
                return agent_request
            except Exception as e:
                logger.debug(f"Completion model failed to run: {e}")
                try_count += 1

        raise ValueError("Completions model failed to run successfully.")

    async def aexecute(self, prompt: PromptSession, agent_id: AgentID = None) -> AgentRequest:
        try_count = 0
        while (try_count <= self._retries):
            try:
                _r = await self._model.arun(prompt)
                agent_request = AgentRequest(
                    agent_id=agent_id,
                    request_id=uuid4(),
                    request_params=_r.request_params,
                    prompt=prompt.session,
                    completion=_r.completion,
                    metadata=_r.metadata)
                return agent_request
            except Exception as e:
                logger.debug(f"Completion model failed to run: {e}")
                try_count += 1

        raise ValueError("Completions model failed to run successfully.")
