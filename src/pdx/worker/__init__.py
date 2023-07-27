from typing import Union
from uuid import uuid4
from pdx.prompt import Prompt
from pdx.models.model import Model
from pdx.prompt.prompt_chain import PromptChain
from pdx.prompt.prompt_tree import PromptTree
from pdx.prompt.prompt_session import PromptSession
from pdx.models.metadata import ModelResponse
from pdx.worker.metadata import WorkerID, RequestMetadata, WorkerResponse, WorkerResponseMetadata


class Worker:
    def __init__(self, prompt: Union[Prompt, PromptChain, PromptTree], model: Model):

        self._prompt = prompt
        self._model = model
        self._worker_id = WorkerID(worker_name='worker_name')

    def _postprocess(self, response: ModelResponse, request: dict, prompt_session: PromptSession) -> WorkerResponse:
        request_metadata = RequestMetadata(
            worker_id=self._worker_id,
            request_id=uuid4(),
            request_values=request,
            request_params=response.request_params,
            prompt=prompt_session.export()
        )
        metadata = WorkerResponseMetadata(
            request=request_metadata,
            response=response.metadata
        )
        worker_response = WorkerResponse(
            data=response.data,
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
        _prompt_session = self._prompt.execute(request)
        _model_response = self._model.execute(_prompt_session)
        _worker_response = self._postprocess(
            _model_response, request, _prompt_session)
        _worker_response.metadata.add_custom(metadata=metadata)
        return _worker_response
