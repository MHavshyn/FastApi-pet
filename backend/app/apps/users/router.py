from apps.auth.dependencies import get_admin_user, get_current_user
from apps.core.dependencies import get_async_session
from apps.users.schemas import RegisteredUserSchema, RegisterUserSchema
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import User, user_manager

router_users = APIRouter()


@router_users.post("/create", status_code=status.HTTP_201_CREATED)
async def create_users(
    new_uses: RegisterUserSchema, session: AsyncSession = Depends(get_async_session)
) -> RegisteredUserSchema:
    created_user = await user_manager.create_user(new_uses, session)
    return created_user


@router_users.get("/user-info")
async def get_user_info(user: User = Depends(get_current_user)) -> RegisteredUserSchema:
    return RegisteredUserSchema.from_orm(user)


@router_users.get("/{id}", dependencies=[Depends(get_admin_user)])
async def get_user(
    user_id: int = Path(..., description="User id", ge=1, alias="id"),
    session: AsyncSession = Depends(get_async_session),
) -> RegisteredUserSchema:
    user: User | None = await user_manager.get(
        session=session, field=User.id, field_value=int(user_id)
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User with given email not found",
        )

    return RegisteredUserSchema.from_orm(user)
