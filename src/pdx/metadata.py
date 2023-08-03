from pydantic import BaseModel


class PDXMetadata(BaseModel):
    version: str = '0.7.0'
