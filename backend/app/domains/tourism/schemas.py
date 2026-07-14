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
