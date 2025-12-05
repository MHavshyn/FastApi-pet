from apps.core.dependencies import get_async_session
from apps.users.crud import User, user_manager
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

router_auth = APIRouter()


@router_auth.post("/loging")
async def user_loging(
    data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    user = await user_manager.get(
        session=session, field=User.email, field_value=data.username
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return {"data": [data.password, data.username]}
