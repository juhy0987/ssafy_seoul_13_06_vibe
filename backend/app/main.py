from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.domains.chat.router import router as chat_router
from app.domains.comments.router import router as comments_router
from app.domains.posts.router import router as posts_router
from app.domains.tourism.router import router as tourism_router

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "posts", "description": "익명 게시판 CRUD · 검색 · 조회수 · 비밀번호 확인"},
    {"name": "comments", "description": "게시글 종속 익명 댓글 CRUD · 비밀번호 확인"},
    {"name": "tourism", "description": "서울 지역 관광지 · 문화시설 · 축제 데이터 조회"},
    {"name": "chat", "description": "서울 지역 정보 질의응답"},
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
app.include_router(comments_router)
app.include_router(tourism_router)
app.include_router(chat_router)


@app.get("/health")
def health():
    return {"status": "ok"}
