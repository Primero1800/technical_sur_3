import logging
from typing import Annotated, Optional, Generator, Self

from fastapi import Header, Request, HTTPException, status
from pydantic import BaseModel

alias: str = "header-param-1"


def get_header_with_alias(
    param: Annotated[
        Optional[str], Header(
            alias=alias
        )
    ] = None
):
    return {
        "key": alias,
        "value": param or "default1",
    }


def get_header_with_alias_parameterized(
    alias: Optional[str] = "header-param-parameterized-3",
):
    async def dependency(
        param: Annotated[
            Optional[str], Header(
                alias=alias,
            )
        ] = None
    ):
        return {
            "key": alias,
            "value": param or "default3",
        }
    return dependency


class Depender:
    name: str
    default: str

    def as_dict(self) -> dict[str, str]:
        return {
            'name': self.name,
            'default': self.default,
        }

    def __str__(self):
        return f"{self.as_dict()}"


    def __repr__(self):
        return str(self)

    def __init__(
            self,
            name: Annotated[str, Header(alias="x-depender-name")],
            default: Annotated[str, Header(alias="x-depender-default")],
    ) -> None:
        self.name = name
        self.default = default
        super().__init__()


class PathReaderDependency:
    def __init__(self, source: str) -> None:
        self.source = source
        self._request: Request | None = None
        self._as_def_head: str | None = None

    async def as_dependency(
            self,
            request: Request,
            as_def_head: Annotated[str, Header(alias="x-as-def-head")] = "foo-as-def-head"
    ) -> Generator[Self, None, None]:
        self._request = request
        self._as_def_head = as_def_head
        yield self
        self._request = None
        self._as_def_head = None

    @property
    def path(self) -> str:
        if self._request is None:
            return ''
        return self._request.url.path

    def read(self, **kwargs: str) -> dict[str, str]:
        return {
            "source": self.source,
            "path": self.path,
            "request_url": str(self._request.url),
            "request_headers": dict(self._request.headers),
            "as_def_head": self._as_def_head,
            **kwargs
        }


path_reader = PathReaderDependency(source='path/api/vog/los')


class TokenIntrospectSchema(BaseModel):
    name: str
    id: int


class HeaderAccessDependency:
    def __init__(self, secret_token: str) -> None:
        self._secret_token = secret_token

    def validate(self, token: str) -> TokenIntrospectSchema:
        if token != self._secret_token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'Token {token} is invalid'
            )
        return TokenIntrospectSchema(
            name='Ivan',
            id=1
        )

    async def __call__(self, token: Annotated[str, Header()]) -> TokenIntrospectSchema:
        token_data = self.validate(token)
        logging.info("!!!!! token validated !!!!!!")
        return token_data


header_access_dependency = HeaderAccessDependency(secret_token='secret_token')