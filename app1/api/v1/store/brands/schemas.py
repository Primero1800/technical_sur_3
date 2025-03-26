from typing import Annotated, TYPE_CHECKING

from pydantic import BaseModel, Field


class BaseBrand(BaseModel):
    title: Annotated[str, Field(
        min_length=3, max_length=100,
        title="Brand's title",
        description="Brand's title that used in application"
    )]
    description: Annotated[str, Field(
        max_length=500,
        title="Brand's description",
        description="Brand's description that used in application"
    )]


class BrandCreate(BaseBrand):
    pass


class BrandRead(BaseBrand):
    id: int
    image_url: str


class BrandUpdate(BaseBrand):
    pass