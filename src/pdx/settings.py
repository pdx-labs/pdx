from pydantic import BaseModel


class Process(BaseModel):
    env: str = 'dev'
    verbose: bool = False


process = Process()
