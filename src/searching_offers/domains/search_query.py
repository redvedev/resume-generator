from pydantic import BaseModel, Field


class SearchQuery(BaseModel):
    pass


class LinkedinSearchQuery(SearchQuery):
    keywords: list[str]
    geo_id: str = Field(alias="geoId", by_alias=True)
    distance: int
