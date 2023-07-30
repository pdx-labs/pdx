from pydantic import BaseModel


class PDXMetadata(BaseModel):
    version: str = '0.6.0'
