from pydantic import BaseModel


class Spot(BaseModel):
    id: str
    title: str
    address: str | None = None
    tel: str | None = None
    image: str | None = None
    thumbnail: str | None = None
    lat: float | None = None
    lng: float | None = None


class SpotListResponse(BaseModel):
    region: str
    contentType: str
    contentTypeId: int
    total: int
    items: list[Spot]


class SpotMetaResponse(BaseModel):
    region: str
    contentType: str
    contentTypeId: int
    total: int


class SpotCategoryCount(BaseModel):
    dataset: str  # 한글 카테고리명(관광지 등)
    contentType: str
    contentTypeId: int
    total: int


class SpotSummaryResponse(BaseModel):
    region: str
    total: int  # 전체 카테고리 장소 수 합계
    categories: list[SpotCategoryCount]
