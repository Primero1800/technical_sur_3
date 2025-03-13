from fastapi import APIRouter, Header

router = APIRouter()


@router.get("/single-direct-dependency")
async def single_direct_dependency(
        header_param: str = Header()
):
    return {
        "header_param": header_param,
    }
