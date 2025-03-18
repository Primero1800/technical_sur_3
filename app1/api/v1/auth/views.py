from fastapi import APIRouter, Request, Body, Depends, HTTPException
from fastapi_users import BaseUserManager, exceptions, models
from pydantic import EmailStr
from starlette import status

from app1.api.v1.users.schemas import UserRead, UserCreate

from app1.core.auth.fastapi_users_config import (
    fastapi_users, authentication_backend,
)
from app1.core.auth.user_manager import get_user_manager


router = APIRouter()

# /login
# /logout
router.include_router(
    fastapi_users.get_auth_router(
        authentication_backend,
        requires_verification=True,
    )
)

# /register
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)


# /request-verify-token
# /verify

@router.post(
        "/request-verify-token",
        status_code=status.HTTP_202_ACCEPTED,
        name="verify:request-token",
    )
async def request_verify_token(
    request: Request,
    email: EmailStr = Body(..., embed=True),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
):
    try:
        user = await user_manager.get_by_email(email)
        await user_manager.request_verify(user, request)
    except exceptions.UserNotExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email {email!r} isn't bound to any user."
        )
    except exceptions.UserInactive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user.email!r} is inactive."
        )
    except exceptions.UserAlreadyVerified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User {user.email!r} is already verified"
        )

    return None


router.include_router(
    fastapi_users.get_verify_router(UserRead),
)


# /forgot-password
# /reset-password
router.include_router(
    fastapi_users.get_reset_password_router(),
)
