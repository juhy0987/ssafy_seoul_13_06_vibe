from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    # 게시글은 특정 장소(spot)에 종속. category·spot_name은 장소 데이터에서 복사한 반정규화 필드.
    category: Mapped[str] = mapped_column(String(20), index=True)
    spot_id: Mapped[str] = mapped_column(String(20), index=True)
    spot_name: Mapped[str] = mapped_column(String(200))
    title: Mapped[str] = mapped_column(String(200))
    content: Mapped[str] = mapped_column(Text)
    # 교육 목적의 의도된 설계: 평문 저장, 응답에는 절대 노출하지 않는다.
    password: Mapped[str] = mapped_column(String(100))
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
