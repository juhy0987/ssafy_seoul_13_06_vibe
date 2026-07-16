from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class PostCategory(str, Enum):
    attraction = "관광지"
    sports = "레포츠"
    culture = "문화시설"
    shopping = "쇼핑"
    lodging = "숙박"
    course = "여행코스"
    festival = "축제공연행사"


class PostCreate(BaseModel):
    category: PostCategory
    spot_id: str = Field(min_length=1, max_length=20)  # 참조 장소 contentid
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    password: str = Field(min_length=1, max_length=100)


class PostUpdate(BaseModel):
    category: PostCategory
    spot_id: str = Field(min_length=1, max_length=20)
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    password: str = Field(min_length=1, max_length=100)


class PasswordCheck(BaseModel):
    password: str = Field(min_length=1, max_length=100)


# 응답 스키마에는 password를 두지 않아 평문 비밀번호 노출을 원천 차단한다.
# spot_name은 장소 데이터에서 복사한 반정규화 필드.
class PostListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: PostCategory
    spot_id: str
    spot_name: str
    title: str
    view_count: int
    like_count: int
    created_at: datetime


class PostDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: PostCategory
    spot_id: str
    spot_name: str
    title: str
    content: str
    view_count: int
    like_count: int
    created_at: datetime
    updated_at: datetime


class PostListResponse(BaseModel):
    total: int
    items: list[PostListItem]


class LikeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    like_count: int
