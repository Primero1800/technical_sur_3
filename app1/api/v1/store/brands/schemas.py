from typing import Annotated, Optional

from pydantic import BaseModel, Field, ConfigDict

base_title_field = Annotated[str, Field(
        min_length=3, max_length=100,
        title="Brand's title",
        description="Brand's title that used in application"
    )]

base_description_field = Annotated[str, Field(
        max_length=500,
        title="Brand's description",
        description="Brand's description that used in application"
    )]


class BaseBrand(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: base_title_field
    description: base_description_field


class BrandCreate(BaseBrand):
    pass


class BrandRead(BaseBrand):
    id: int
    image_file: str


class BrandUpdate(BaseBrand):
    pass


class BrandPartialUpdate(BaseBrand):
    title: Optional[base_title_field] = None
    description: Optional[base_description_field] = None
