"""LangChain LCEL RAG 파이프: 하이브리드 검색(관광 벡터 + 게시글 키워드) → prompt → LLM.

`answer(message, history)` 형태로 기존 chat.service 인터페이스와 호환된다.
- 관광 데이터: sqlite 벡터 스토어 의미 검색(정적)
- 커뮤니티 게시글: DB 키워드 검색(동적 → 항상 최신, 평문 비밀번호 미포함)
"""
from functools import lru_cache
from pathlib import Path

from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
# from langchain_openai import ChatOpenAI  # 테스트를 위해 Gemini로 대체(주석 처리)
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import settings
from app.domains.chat.rag.embeddings import get_embeddings
from app.domains.chat.rag.store import SQLiteRetriever, SQLiteVectorStore
from app.domains.posts import service as post_service

PROMPT_DIR = Path(__file__).resolve().parents[1] / "prompts"

HUMAN_TEMPLATE = (
    "<context>\n{context}\n</context>\n\n"
    "이전 대화:\n{history}\n\n"
    "질문: {question}"
)


@lru_cache(maxsize=1)
def _retriever() -> SQLiteRetriever:
    return SQLiteRetriever(store=SQLiteVectorStore(get_embeddings()), k=settings.rag_top_k)


def _format_context(spot_docs: list[Document], posts: list[dict]) -> str:
    lines = []
    for doc in spot_docs:
        meta = doc.metadata
        lines.append(f"- [{meta['category']}] {meta['title']} · {meta.get('address') or '주소 정보 없음'}")
    for post in posts:
        snippet = (post.get("content") or "").strip().replace("\n", " ")[:80]
        lines.append(f"- [게시글] {post['title']} (장소: {post['spot_name']}) · {snippet}")
    return "\n".join(lines) if lines else "(관련 데이터 없음)"


def _retrieve_context(question: str) -> str:
    spot_docs = _retriever().invoke(question)
    posts = post_service.search_posts(question, limit=settings.rag_top_k)
    return _format_context(spot_docs, posts)


def _format_history(history: list[dict] | None) -> str:
    if not history:
        return "(없음)"
    return "\n".join(f"{turn.get('role')}: {turn.get('content')}" for turn in history[-4:])


@lru_cache(maxsize=1)
def _chain():
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", (PROMPT_DIR / "rag_system.md").read_text(encoding="utf-8")),
            ("human", HUMAN_TEMPLATE),
        ]
    )
    # llm = ChatOpenAI(model=settings.chat_model, temperature=0.3, api_key=settings.openai_api_key)
    llm = ChatGoogleGenerativeAI(
        model=settings.gemini_model, temperature=0.3, google_api_key=settings.google_api_key
    )
    return (
        RunnableParallel(
            context=RunnableLambda(lambda x: _retrieve_context(x["question"])),
            question=RunnableLambda(lambda x: x["question"]),
            history=RunnableLambda(lambda x: _format_history(x.get("history"))),
        )
        | prompt
        | llm
        | StrOutputParser()
    )


def answer(message: str, history: list[dict] | None = None) -> str:
    return _chain().invoke({"question": message, "history": history or []})
