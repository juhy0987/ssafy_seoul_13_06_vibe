import json
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./localhub.db"
    # NoDecode: pydantic-settings 의 JSON 강제 파싱을 끈다.
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:5173"]

    # 챗봇 RAG
    openai_api_key: str | None = None
    chat_model: str = "gpt-5-mini"
    embedding_model: str = "jhgan/ko-sroberta-multitask"
    rag_top_k: int = 10

    @field_validator("cors_origins", mode="before")
    @classmethod
    def _parse_cors_origins(cls, value):
        if not isinstance(value, str):
            return value
        text = value.strip()
        if not text:
            return []
        if text.startswith("["):  # JSON 배열 형태도 그대로 수용
            return json.loads(text)
        return [origin.strip() for origin in text.split(",") if origin.strip()]


settings = Settings()
