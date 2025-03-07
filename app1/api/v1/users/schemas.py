from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

base_username_field = Annotated[str, Field(
        min_length=3, max_length=32,
        default='username',
        title='User name',
        description='The alias of user, that uses in application',
    )]


base_foo_field = Annotated[str, Field(
        min_length=2, max_length=8,
        default='foo',
        title='User foo',
        description='The alias of foo, that uses in application',
    )]

base_bar_field = Annotated[str, Field(
        min_length=2, max_length=8,
        default='bar',
        title='User foo',
        description='The alias of foo, that uses in application',
    )]


class UserBase(BaseModel):
    username: base_username_field
    foo: base_foo_field
    bar: base_bar_field

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id if hasattr(self, 'id') else None}, username={self.username})"

    def __repr__(self):
        return str(self)


class UserRead(UserBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id: int
    indicator: str = 'schemas.user_read'


class UserCreate(UserBase):
    pass
