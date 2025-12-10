from apps.auth.dependencies import require_permissions
from apps.core.dependencies import get_async_session
from apps.products.crud import Category, category_manager
from apps.products.schemas import NewCategory, SavedCategorySchema
from apps.users.constants import UserPermissionsEnum
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router_categories = APIRouter()


@router_categories.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permissions([UserPermissionsEnum.CAN_CREATE_CATEGORY]))
    ],
)
async def create_category(
    new_category: NewCategory, session: AsyncSession = Depends(get_async_session)
) -> SavedCategorySchema:
    maybe_category = await category_manager.get(
        session=session, field=Category.name, field_value=new_category.name
    )
    if maybe_category:
        raise HTTPException(
            detail="Category with this name already exists",
            status_code=status.HTTP_409_CONFLICT,
        )
    saved_category = await category_manager.create(
        **new_category.model_dump(), session=session
    )
    return saved_category
