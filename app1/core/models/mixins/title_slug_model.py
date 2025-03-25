from pydantic import computed_field
from slugify import slugify


class TitleSlugModel:

    @computed_field
    @property
    def slug(self) -> str:
        return slugify(self.title)
