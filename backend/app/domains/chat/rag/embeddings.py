import time
from functools import lru_cache

import numpy as np
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings


def _normalize(vectors) -> np.ndarray:
    arr = np.asarray(vectors, dtype=np.float32)
    norms = np.clip(np.linalg.norm(arr, axis=1, keepdims=True), 1e-9, None)
    return arr / norms


class GoogleEmbeddings(Embeddings):
    """Google AI Studio(무료 티어) 임베딩 API.

    - 코사인=내적을 위해 L2 정규화한다.
    - 무료 티어는 배치 미지원 → 요청당 1건(embedContent). 각 요청 사이에 최소 60/RPM 초
      간격을 두어 분당 호출 제한(RPM)을 준수한다(과속 시 sleep).
    """

    def __init__(self):
        self._embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key,
        )
        self._min_interval = 60.0 / max(settings.embedding_rpm, 1)
        self._last = 0.0

    def _throttle(self) -> None:
        wait = self._min_interval - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        self._last = time.monotonic()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        # 무료 티어는 배치(batchEmbedContents) 미지원 → 표준 단건(embedContent) 요청을 순차 처리
        vectors = [self._embed_one(text) for text in texts]
        return _normalize(vectors).tolist()

    def _embed_one(self, text: str) -> list[float]:
        self._throttle()  # 요청 전 대기(분당 상한 준수)
        return self._embeddings.embed_query(text)

    def embed_query(self, text: str) -> list[float]:
        return _normalize([self._embed_one(text)])[0].tolist()


@lru_cache(maxsize=1)
def get_embeddings() -> GoogleEmbeddings:
    """최초 호출 시 Google 임베딩 클라이언트를 초기화한다(GOOGLE_API_KEY 필요)."""
    return GoogleEmbeddings()
