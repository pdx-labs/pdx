from dataclasses import dataclass


@dataclass
class ModelTokenUsage:
    response: int = None
    prompt: int = None
    total: int = None


@dataclass
class ResponseMetadata:
    model: str
    api_log_id: str = None
    stop: str = None
    stop_reason: str = None
    token_usage: ModelTokenUsage = None
    latency: float = None

@dataclass
class ModelResponse:
    metadata: ResponseMetadata = None
    request_params: dict = None
    data: str = None
    