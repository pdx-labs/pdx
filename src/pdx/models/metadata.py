from dataclasses import dataclass


@dataclass
class ModelTokenUsage:
    completion: int = None
    prompt: int = None
    total: int = None


@dataclass
class ResponseMetadata:
    model: str
    api_log_id: str = None
    stop: str = None
    stop_reason: str = None
    token_usage: ModelTokenUsage = None
    completion_time: float = None

@dataclass
class ModelResponse:
    metadata: ResponseMetadata = None
    request_params: dict = None
    completion: str = None
    