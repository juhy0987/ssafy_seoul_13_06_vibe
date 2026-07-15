from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    content: str = Field(min_length=1)
    password: str = Field(min_length=1, max_length=100)


class CommentUpdate(BaseModel):
    content: str = Field(min_length=1)
    password: str = Field(min_length=1, max_length=100)


class PasswordCheck(BaseModel):
    password: str = Field(min_length=1, max_length=100)


# 응답 스키마에는 password를 두지 않아 평문 비밀번호 노출을 원천 차단한다.
class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: int
    content: str
    created_at: datetime
    updated_at: datetime
