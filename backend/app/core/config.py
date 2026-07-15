from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./localhub.db"
    cors_origins: list[str] = ["http://localhost:5173"]

    # 챗봇 RAG
    openai_api_key: str | None = None
    chat_model: str = "gpt-5-mini"
    embedding_model: str = "jhgan/ko-sroberta-multitask"
    rag_top_k: int = 10


settings = Settings()
