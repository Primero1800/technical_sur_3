from typing import Annotated, Optional

from fastapi import APIRouter, Header, Depends, Response, Request
from starlette.responses import JSONResponse

from .dependencies import (
    get_header_with_alias,
    get_header_with_alias_parameterized,
)


router = APIRouter()


@router.get("/single-direct-dependency")
async def single_direct_dependency(
        header_param: dict = Depends(get_header_with_alias)
):
    return {
        header_param["key"]: header_param["value"],
    }


alias2: str = "header-param-2"


@router.get("/multi-dependency")
async def single_direct_dependency(
        response: Response,
        header_param: dict = Depends(get_header_with_alias),
        header_param2: Annotated[
                       Optional[str],
                       Header(alias=alias2),
                    ] = "default2",
        header_param3: dict = Depends(get_header_with_alias_parameterized())
):
    response.headers[header_param["key"]] = header_param["value"]
    response.headers[alias2] = header_param2
    response.headers[header_param3["key"]] = header_param3["value"]
    return JSONResponse(
        content=dict(response.headers),
        headers=response.headers
    )
