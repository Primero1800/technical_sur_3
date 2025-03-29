from typing import Annotated, Optional, Any, List
from pydantic import BaseModel, Field, ConfigDict, model_validator
from pydantic_core.core_schema import ValidationInfo

from app1.api.v1.store.mixins import TitleSlugMixin


base_title_field = Annotated[str, Field(
        min_length=3, max_length=100,
        title="Product's title",
        description="Product's title that used in application"
    )]

base_description_field = Annotated[str, Field(
        max_length=500,
        title="Product's description",
        description="Product's description that used in application"
    )]


class BaseProduct(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: base_title_field
    description: base_description_field

    brand_id: int
    rubric_ids: List[int]


class ProductCreate(BaseProduct, TitleSlugMixin):
    pass


class ProductRead(BaseProduct):
    id: int
    # image_file: str
    slug: str
    rubrics: List[Any]
    images: List[Any]
    brand: Any


    # @model_validator(mode="before")
    # @classmethod
    # def image_file_getter(cls, obj: Any, info: ValidationInfo) -> Any:
    #     if not hasattr(obj, "image_file") and info.context:
    #         setattr(obj, 'image_file', info.context.get('image_file', ''))
    #     return obj


class ProductUpdate(BaseProduct, TitleSlugMixin):
    pass


class ProductPartialUpdate(BaseProduct, TitleSlugMixin):
    pass
    # title: Optional[base_title_field] = None
    # description: Optional[base_description_field] = None
