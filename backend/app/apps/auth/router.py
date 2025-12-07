from apps.auth.auth_handler import auth_handler
from apps.auth.dependencies import get_current_user
from apps.auth.schemas import ForceLogoutSchema, LoginResponseSchema
from apps.core.dependencies import get_async_session
from apps.users.crud import user_manager
from apps.users.models import User
from fastapi import APIRouter, Depends, Header, status
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


@router_auth.post("/force-logout", status_code=status.HTTP_204_NO_CONTENT)
async def force_logout(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await user_manager.patch(
        instance_id=user.id,
        data_to_patch=ForceLogoutSchema(),
        session=session,
        exclude_unset=False,
    )
