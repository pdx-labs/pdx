from pydantic import BaseSettings, BaseModel


class Keys(BaseSettings):
    openai_key: str = None
    anthropic_key: str = None
    cohere_key: str = None


class Process(BaseModel):
    env: str = 'dev'
    verbose: bool = False


process = Process()
