from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class BaseBrand(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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
    image_file: str


class BrandUpdate(BaseBrand):
    pass