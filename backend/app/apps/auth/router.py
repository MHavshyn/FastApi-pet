from apps.auth.auth_handler import auth_handler
from apps.auth.schemas import LoginResponseSchema
from apps.core.dependencies import get_async_session
from fastapi import APIRouter, Depends, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router_auth = APIRouter()


@router_auth.post("/login")
async def user_loging(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> LoginResponseSchema:
    # user = await user_manager.get(
    #     session=session, field=User.email, field_value=data.username
    # )
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    #     )

    login_response: LoginResponseSchema = await auth_handler.get_login_token_pairs(
        session=session, data=data
    )

    return login_response


@router_auth.post("/refresh")
async def refresh_user_token(
    refresh_token: str = Header(alias="X-Refresh-Token"),
    session: AsyncSession = Depends(get_async_session),
) -> LoginResponseSchema:
    token_pair = await auth_handler.get_refresh_tokens(
        refresh_token=refresh_token, session=session
    )
    return token_pair
