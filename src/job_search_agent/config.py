from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    langsmith_tracing: bool
    langsmith_api_key: str
    tavily_api_key: str

    llm_model: str
    model_provider: str
    croq_api_key: str
    
    runtime_env: str 
    web_search_test_data_file: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")