from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domains.comments import schemas, service

# 댓글은 게시글에 종속 — 경로에 그대로 반영
router = APIRouter(prefix="/api/posts/{post_id}/comments", tags=["comments"])

NOT_FOUND = {404: {"description": "게시글 또는 댓글을 찾을 수 없음"}}
PW_MISMATCH = {403: {"description": "비밀번호 불일치"}, **NOT_FOUND}


@router.get("", response_model=list[schemas.CommentOut], summary="댓글 목록 조회", responses=NOT_FOUND)
def list_comments(post_id: int, db: Session = Depends(get_db)):
    return service.list_comments(db, post_id)


@router.post(
    "",
    response_model=schemas.CommentOut,
    status_code=status.HTTP_201_CREATED,
    summary="댓글 작성",
    responses=NOT_FOUND,
)
def create_comment(post_id: int, data: schemas.CommentCreate, db: Session = Depends(get_db)):
    return service.create_comment(db, post_id, data)


@router.put(
    "/{comment_id}",
    response_model=schemas.CommentOut,
    summary="댓글 수정 (비밀번호 필요)",
    responses=PW_MISMATCH,
)
def update_comment(
    post_id: int, comment_id: int, data: schemas.CommentUpdate, db: Session = Depends(get_db)
):
    return service.update_comment(db, post_id, comment_id, data)


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="댓글 삭제 (비밀번호 필요)",
    responses=PW_MISMATCH,
)
def delete_comment(
    post_id: int, comment_id: int, body: schemas.PasswordCheck, db: Session = Depends(get_db)
):
    service.delete_comment(db, post_id, comment_id, body.password)
