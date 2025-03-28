from typing import TYPE_CHECKING

from .schemas import RubricRead

if TYPE_CHECKING:
    from app1.core.models import Rubric


async def get_schema_from_orm(
    orm_model: "Rubric"
) -> RubricRead:
    image_file = orm_model.image.file if hasattr(orm_model.image, "file") else ''

    return RubricRead.model_validate(
        obj=orm_model,
        from_attributes=True,
        context={"image_file": image_file},
    )

    # BRUTE FORCE VARIANT
    # return RubricRead(**orm_model.to_dict(), image_file=image_file)
