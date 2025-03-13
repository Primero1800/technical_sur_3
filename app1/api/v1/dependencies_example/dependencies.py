from typing import Annotated, Optional

from fastapi import Header


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
