from typing import Optional, Any, Union, List
from pydantic import BaseModel, Field


class ModelTokenUsage(BaseModel):
    response: Optional[int] = Field(default=None)
    prompt: Optional[int] = Field(default=None)
    total: Optional[int] = Field(default=None)


class ResponseMetadata(BaseModel):
    model: str
    api_log_id: Optional[str] = Field(default=None)
    stop: Optional[str] = Field(default=None)
    stop_reason: Optional[str] = Field(default=None)
    warnings: Optional[Any] = Field(default=None)
    token_usage: Optional[ModelTokenUsage] = Field(default=ModelTokenUsage())
    latency: Optional[float] = Field(default=None)
    other: Optional[Any] = Field(default=None)


class ModelResponse(BaseModel):
    metadata: Optional[ResponseMetadata] = Field(default=None)
    request_params: Optional[dict] = Field(default=None)
    data_type: str = Field(default='text')
    data: Union[Any, str, list, bytes, List[bytes]]
