from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.comments import schemas
from app.domains.comments.models import Comment
from app.domains.posts.models import Post


def _ensure_post(db: Session, post_id: int) -> None:
    if db.get(Post, post_id) is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "게시글을 찾을 수 없습니다.")


def _get_or_404(db: Session, post_id: int, comment_id: int) -> Comment:
    comment = db.get(Comment, comment_id)
    if comment is None or comment.post_id != post_id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "댓글을 찾을 수 없습니다.")
    return comment


def _verify_password(comment: Comment, password: str) -> None:
    # 인증 없는 익명 커뮤니티: 평문 비밀번호 일치 여부로만 권한을 확인한다.
    if comment.password != password:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "비밀번호가 일치하지 않습니다.")


def list_comments(db: Session, post_id: int) -> list[Comment]:
    _ensure_post(db, post_id)
    return list(
        db.scalars(
            select(Comment).where(Comment.post_id == post_id).order_by(Comment.id.asc())
        ).all()
    )


def create_comment(db: Session, post_id: int, data: schemas.CommentCreate) -> Comment:
    _ensure_post(db, post_id)
    comment = Comment(post_id=post_id, content=data.content, password=data.password)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def update_comment(db: Session, post_id: int, comment_id: int, data: schemas.CommentUpdate) -> Comment:
    comment = _get_or_404(db, post_id, comment_id)
    _verify_password(comment, data.password)
    comment.content = data.content
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, post_id: int, comment_id: int, password: str) -> None:
    comment = _get_or_404(db, post_id, comment_id)
    _verify_password(comment, password)
    db.delete(comment)
    db.commit()
