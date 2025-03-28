from typing import Annotated, Optional, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator
from pydantic_core.core_schema import ValidationInfo

from app1.api.v1.store.mixins import TitleSlugMixin


base_title_field = Annotated[str, Field(
        min_length=3, max_length=100,
        title="Rubric's title",
        description="Rubric's title that used in application"
    )]

base_description_field = Annotated[str, Field(
        max_length=500,
        title="Rubric's description",
        description="Rubric's description that used in application"
    )]


class BaseRubric(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: base_title_field
    description: base_description_field


class RubricCreate(BaseRubric, TitleSlugMixin):
    pass


class RubricRead(BaseRubric):
    id: int
    image_file: str
    slug: str

    @model_validator(mode="before")
    @classmethod
    def image_file_getter(cls, obj: Any, info: ValidationInfo) -> Any:
        if not hasattr(obj, "image_file") and info.context:
            setattr(obj, 'image_file', info.context.get('image_file', ''))
        return obj


class RubricUpdate(BaseRubric, TitleSlugMixin):
    pass


class RubricPartialUpdate(BaseRubric, TitleSlugMixin):
    title: Optional[base_title_field] = None
    description: Optional[base_description_field] = None
