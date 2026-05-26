from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    opensearch_host: str = "localhost"
    opensearch_port: int = 9200
    opensearch_user: str = "admin"
    opensearch_password: str = "Admin@12345"

    ollama_host: str = "http://localhost:11434"
    embed_model: str = "nomic-embed-text"
    llm_model: str = "qwen3"
    embed_dimension: int = 768

    trigger_latency_multiplier: float = 3.0
    trigger_error_rate_threshold: float = 0.3
    trigger_retry_threshold: int = 4
    trigger_token_spike_threshold: int = 20000


settings = Settings()
