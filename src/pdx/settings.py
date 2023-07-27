from pydantic import BaseSettings, BaseModel


class Process(BaseModel):
    env: str = 'dev'
    verbose: bool = False


process = Process()
