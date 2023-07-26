import uuid
import subprocess
from dataclasses import dataclass, field
from pdx.metadata import PDXMetadata
from pdx.models.metadata import ResponseMetadata
from pdx.logger import logger


@dataclass
class WorkerID:
    worker_name: str
    git_hash: str = None
    git_branch: str = None

    def __post_init__(self):
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


@dataclass
class RequestMetadata:
    worker_id: WorkerID
    request_id: uuid.UUID = None
    request_values: dict = None
    request_params: dict = None
    prompt: list = None

    def __post_init__(self):
        if self.request_id is None:
            self.request_id = uuid.uuid4()


@dataclass
class WorkerResponseMetadata:
    request: RequestMetadata
    response: ResponseMetadata
    custom: dict = None
    pdx: PDXMetadata = None

    def __post_init__(self):
        if self.pdx is None:
            self.pdx = PDXMetadata()

    def add_custom(self, metadata: dict):
        self.custom = metadata


@dataclass
class WorkerResponse:
    data: str
    metadata: WorkerResponseMetadata
