from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    langsmith_tracing: bool
    langsmith_api_key: str
    tavily_api_key: str

    llm_model: str
    model_provider: str
    croq_api_key: str

    llm_agent_retry_enabled: bool

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")