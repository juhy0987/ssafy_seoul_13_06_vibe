from fastapi import HTTPException, status
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.domains.posts import schemas
from app.domains.posts.models import Post
from app.domains.tourism import service as tourism


def _get_or_404(db: Session, post_id: int) -> Post:
    post = db.get(Post, post_id)
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "게시글을 찾을 수 없습니다.")
    return post


def _verify_password(post: Post, password: str) -> None:
    # 인증 없는 익명 커뮤니티: 평문 비밀번호 일치 여부로만 권한을 확인한다.
    if post.password != password:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "비밀번호가 일치하지 않습니다.")


def _resolve_spot_name(category: schemas.PostCategory, spot_id: str) -> str:
    name = tourism.get_spot_name(category.value, spot_id)
    if name is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "존재하지 않는 장소입니다.")
    return name


def list_posts(
    db: Session,
    category: schemas.PostCategory | None,
    spot_id: str | None,
    q: str | None,
    page: int,
    size: int,
) -> schemas.PostListResponse:
    conditions = []
    if category:
        conditions.append(Post.category == category.value)
    if spot_id:
        conditions.append(Post.spot_id == spot_id)
    if q:
        keyword = f"%{q}%"
        # 반정규화된 spot_name 덕분에 장소명 검색도 조인 없이 처리된다.
        conditions.append(
            Post.title.ilike(keyword) | Post.content.ilike(keyword) | Post.spot_name.ilike(keyword)
        )

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


def like_post(db: Session, post_id: int) -> Post:
    post = _get_or_404(db, post_id)
    post.like_count += 1
    db.commit()
    db.refresh(post)
    return post


def unlike_post(db: Session, post_id: int) -> Post:
    post = _get_or_404(db, post_id)
    if post.like_count > 0:  # 익명 좋아요: 0 미만으로 내려가지 않도록 방어
        post.like_count -= 1
        db.commit()
        db.refresh(post)
    return post


def create_post(db: Session, data: schemas.PostCreate) -> Post:
    spot_name = _resolve_spot_name(data.category, data.spot_id)
    post = Post(
        category=data.category.value,
        spot_id=data.spot_id,
        spot_name=spot_name,
        title=data.title,
        content=data.content,
        password=data.password,
    )
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def update_post(db: Session, post_id: int, data: schemas.PostUpdate) -> Post:
    post = _get_or_404(db, post_id)
    _verify_password(post, data.password)
    post.spot_name = _resolve_spot_name(data.category, data.spot_id)
    post.category = data.category.value
    post.spot_id = data.spot_id
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


def search_posts(query: str, limit: int = 5) -> list[dict]:
    """챗봇 RAG용 게시글 키워드 검색(제목·내용·장소명). 평문 비밀번호는 절대 포함하지 않는다."""
    keywords = tourism.tokenize(query)
    if not keywords:
        return []
    conditions = [
        Post.title.ilike(f"%{kw}%") | Post.content.ilike(f"%{kw}%") | Post.spot_name.ilike(f"%{kw}%")
        for kw in keywords
    ]
    with SessionLocal() as db:
        rows = db.scalars(
            select(Post).where(or_(*conditions)).order_by(Post.id.desc()).limit(limit)
        ).all()
        return [
            {
                "id": row.id, "category": row.category, "spot_name": row.spot_name,
                "title": row.title, "content": row.content,
            }
            for row in rows
        ]
