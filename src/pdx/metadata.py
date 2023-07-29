from pydantic import BaseModel


class PDXMetadata(BaseModel):
    version: str = '0.5.0'
