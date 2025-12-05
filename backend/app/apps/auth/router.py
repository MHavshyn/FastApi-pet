from apps.auth.auth_handler import auth_handler
from apps.auth.schemas import LoginResponseSchema
from apps.core.dependencies import get_async_session
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router_auth = APIRouter()


@router_auth.post("/loging")
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
