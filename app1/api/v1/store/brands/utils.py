from typing import TYPE_CHECKING

from app1.api.v1.store.brands.schemas import BrandRead

if TYPE_CHECKING:
    from app1.core.models.store import Brand


async def get_brand_schema_from_orm(
    orm_model: "Brand"
) -> BrandRead:
    image_file = orm_model.image.file if hasattr(orm_model.image, "file") else ''

    return BrandRead.model_validate(
        obj=orm_model,
        from_attributes=True,
        context={"image_file": image_file},
    )

    # BRUTE FORCE VARIANT
    # return BrandRead(**orm_model.to_dict(), image_file=image_file)
