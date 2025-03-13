from typing import Annotated
from pydantic import BaseModel, Field


class DisplayUserNameMixin(BaseModel):

    display_name: Annotated[str, Field(
            max_length=50, min_length=2,
            default="John Doe",
            description="Displayed user's name, used in application",
            title='Displayed user name'
    )]