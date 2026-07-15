import json
from urllib.parse import urlsplit
from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./localhub.db"
    # NoDecode: pydantic-settings 의 JSON 강제 파싱을 끈다.
    cors_origins: Annotated[list[str], NoDecode] = ["http://localhost:5173"]

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

    @field_validator("cors_origins")
    @classmethod
    def normalize_cors_origins(cls, origins: list[str]) -> list[str]:
        normalized: list[str] = []

        for origin in origins:
            origin = origin.strip().rstrip("/")
            parsed = urlsplit(origin)
            if (
                parsed.scheme not in {"http", "https"}
                or not parsed.netloc
                or parsed.path
                or parsed.query
                or parsed.fragment
            ):
                raise ValueError(
                    "CORS_ORIGINS must contain origins only, "
                    "for example https://localhub.netlify.app"
                )
            if origin not in normalized:
                normalized.append(origin)

        if not normalized:
            raise ValueError("CORS_ORIGINS must contain at least one origin")

        return normalized

    # 챗봇 RAG
    openai_api_key: str | None = None
    chat_model: str = "gpt-5-mini"
    embedding_model: str = "jhgan/ko-sroberta-multitask"
    rag_top_k: int = 10


settings = Settings()
