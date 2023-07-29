import uuid
import subprocess
from typing import Union, Optional
from pydantic import BaseModel, Field
from pdx.metadata import PDXMetadata
from pdx.models.metadata import ResponseMetadata
from pdx.logger import logger

AgentRequest = Union[dict, str]


class AgentID(BaseModel):
    agent_name: str = Field(default='agent')
    unique_id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    git_hash: Optional[str] = Field(default=None)
    git_branch: Optional[str] = Field(default=None)

    def model_post_init(self, *args, **kwargs) -> None:
        if self.git_hash is None and self.git_branch is None:
            try:
                subprocess.check_output(
                    ['git', 'rev-parse', '--is-inside-work-tree']).decode('utf-8').strip()
                self.git_hash = subprocess.check_output(
                    ['git', 'rev-parse', 'HEAD']).decode('utf-8').strip()
                self.git_branch = subprocess.check_output(
                    ['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode('utf-8').strip()
            except subprocess.CalledProcessError:
                logger.echo(
                    'Not a git repository. Using default values.', event='warning')
                logger.echo(
                    'It is recommended to run `pdx` from a initialized git repository.', event='warning')
                self.git_hash = 'not-git-repo'
                self.git_branch = 'not-git-repo'


class RequestMetadata(BaseModel):
    agent_id: AgentID
    request_id: uuid.UUID = Field(default_factory=lambda: uuid.uuid4())
    request_values: dict
    request_params: dict
    prompt: list


class AgentResponseMetadata(BaseModel):
    request: RequestMetadata
    response: ResponseMetadata
    pdx: PDXMetadata = Field(default_factory=lambda: PDXMetadata())
    custom: Optional[dict] = None

    def add_custom(self, metadata: dict):
        self.custom = metadata


class AgentResponse(BaseModel):
    data: str
    metadata: AgentResponseMetadata
