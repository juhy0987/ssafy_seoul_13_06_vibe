from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.domains.posts.router import router as posts_router

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "posts", "description": "익명 게시판 CRUD · 검색 · 조회수 · 비밀번호 확인"},
]

app = FastAPI(
    title="LocalHub API",
    description="공공데이터 기반 서울 지역 정보 공유 커뮤니티 백엔드 API",
    version="1.0.0",
    openapi_tags=tags_metadata,
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts_router)


@app.get("/health")
def health():
    return {"status": "ok"}
