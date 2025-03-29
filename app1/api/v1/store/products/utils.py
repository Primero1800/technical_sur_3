from typing import TYPE_CHECKING

from .schemas import ProductRead

if TYPE_CHECKING:
    from app1.core.models import Product


async def get_schema_from_orm(
    orm_model: "Product"
) -> ProductRead:

    # image_file = orm_model.image.file if hasattr(orm_model.image, "file") else ''

    # return ProductRead.model_validate(
    #     obj=orm_model,
    #     from_attributes=True,
    #     context={"image_file": image_file},
    # )

    # BRUTE FORCE VARIANT
    return ProductRead(**orm_model.to_dict())
