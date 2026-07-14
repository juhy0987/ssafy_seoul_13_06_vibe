from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class PostCategory(str, Enum):
    tour = "관광지"
    food = "맛집"
    festival = "축제행사"


class PostCreate(BaseModel):
    category: PostCategory
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    password: str = Field(min_length=1, max_length=100)


class PostUpdate(BaseModel):
    category: PostCategory
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    password: str = Field(min_length=1, max_length=100)


class PasswordCheck(BaseModel):
    password: str = Field(min_length=1, max_length=100)


# 응답 스키마에는 password를 두지 않아 평문 비밀번호 노출을 원천 차단한다.
class PostListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: PostCategory
    title: str
    view_count: int
    created_at: datetime


class PostDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    category: PostCategory
    title: str
    content: str
    view_count: int
    created_at: datetime
    updated_at: datetime


class PostListResponse(BaseModel):
    total: int
    items: list[PostListItem]
