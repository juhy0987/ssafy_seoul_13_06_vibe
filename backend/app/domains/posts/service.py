from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domains.posts import schemas
from app.domains.posts.models import Post


def _get_or_404(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "게시글을 찾을 수 없습니다.")
    return post


def _verify_password(post: Post, password: str) -> None:
    # 인증 없는 익명 커뮤니티: 평문 비밀번호 일치 여부로만 권한을 확인한다.
    if post.password != password:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "비밀번호가 일치하지 않습니다.")


def list_posts(
    db: Session,
    category: schemas.PostCategory | None,
    q: str | None,
    page: int,
    size: int,
) -> schemas.PostListResponse:
    conditions = []
    if category:
        conditions.append(Post.category == category.value)
    if q:
        keyword = f"%{q}%"
        conditions.append(Post.title.ilike(keyword) | Post.content.ilike(keyword))

    total = db.scalar(select(func.count()).select_from(Post).where(*conditions))
    items = db.scalars(
        select(Post)
        .where(*conditions)
        .order_by(Post.id.desc())
        .offset((page - 1) * size)
        .limit(size)
    ).all()
    return schemas.PostListResponse(total=total or 0, items=items)


def get_post(db: Session, post_id: int) -> Post:
    post = _get_or_404(db, post_id)
    post.view_count += 1  # 상세 조회 시 조회수 증가
    db.commit()
    db.refresh(post)
    return post


def create_post(db: Session, data: schemas.PostCreate) -> Post:
    post = Post(**data.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(db: Session, post_id: int, data: schemas.PostUpdate) -> Post:
    post = _get_or_404(db, post_id)
    _verify_password(post, data.password)
    post.title = data.title
    post.content = data.content
    db.commit()
    db.refresh(post)
    return post


def delete_post(db: Session, post_id: int, password: str) -> None:
    post = _get_or_404(db, post_id)
    _verify_password(post, password)
    db.delete(post)
    db.commit()


def verify_post_password(db: Session, post_id: int, password: str) -> None:
    post = _get_or_404(db, post_id)
    _verify_password(post, password)
