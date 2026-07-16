from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domains.posts import schemas, service

router = APIRouter(prefix="/api/posts", tags=["posts"])

NOT_FOUND = {404: {"description": "게시글을 찾을 수 없음"}}
PW_MISMATCH = {403: {"description": "비밀번호 불일치"}, **NOT_FOUND}


@router.get("", response_model=schemas.PostListResponse, summary="게시글 목록 조회")
def list_posts(
    category: schemas.PostCategory | None = Query(default=None, description="카테고리 필터"),
    spot_id: str | None = Query(default=None, description="장소(contentid) 필터"),
    q: str | None = Query(default=None, description="제목·내용·장소명 검색어"),
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    return service.list_posts(db, category, spot_id, q, page, size)


@router.get(
    "/{post_id}",
    response_model=schemas.PostDetail,
    summary="게시글 상세 조회 (조회수 증가)",
    responses=NOT_FOUND,
)
def get_post(post_id: int, db: Session = Depends(get_db)):
    return service.get_post(db, post_id)


@router.post(
    "",
    response_model=schemas.PostDetail,
    status_code=status.HTTP_201_CREATED,
    summary="게시글 작성",
)
def create_post(data: schemas.PostCreate, db: Session = Depends(get_db)):
    return service.create_post(db, data)


@router.put(
    "/{post_id}",
    response_model=schemas.PostDetail,
    summary="게시글 수정 (비밀번호 필요)",
    responses=PW_MISMATCH,
)
def update_post(post_id: int, data: schemas.PostUpdate, db: Session = Depends(get_db)):
    return service.update_post(db, post_id, data)


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="게시글 삭제 (비밀번호 필요)",
    responses=PW_MISMATCH,
)
def delete_post(post_id: int, body: schemas.PasswordCheck, db: Session = Depends(get_db)):
    service.delete_post(db, post_id, body.password)


@router.post(
    "/{post_id}/verify",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="비밀번호 확인 (수정/삭제 진입 전 모달용)",
    responses=PW_MISMATCH,
)
def verify_password(post_id: int, body: schemas.PasswordCheck, db: Session = Depends(get_db)):
    service.verify_post_password(db, post_id, body.password)


@router.post(
    "/{post_id}/like",
    response_model=schemas.LikeResponse,
    summary="좋아요",
    responses=NOT_FOUND,
)
def like_post(post_id: int, db: Session = Depends(get_db)):
    return service.like_post(db, post_id)


@router.delete(
    "/{post_id}/like",
    response_model=schemas.LikeResponse,
    summary="좋아요 취소",
    responses=NOT_FOUND,
)
def unlike_post(post_id: int, db: Session = Depends(get_db)):
    return service.unlike_post(db, post_id)
