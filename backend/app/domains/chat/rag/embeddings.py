from functools import lru_cache

from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import settings


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    """한국어 문장 임베딩(jhgan/ko-sroberta-multitask, 정규화 → 코사인=내적).
    모델명은 settings.embedding_model 로 교체 가능. 최초 호출 시 모델을 로드한다."""
    return HuggingFaceEmbeddings(
        model_name=settings.embedding_model,
        encode_kwargs={"normalize_embeddings": True},
    )
