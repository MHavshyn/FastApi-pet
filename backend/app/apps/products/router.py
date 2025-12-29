import uuid
from typing import Annotated

from apps.auth.dependencies import get_current_user, require_permissions
from apps.core.dependencies import get_async_session
from apps.core.schemas import SearchParamsSchema
from apps.products.crud import (
    Category,
    category_manager,
    order_manager,
    product_manager,
)
from apps.products.dependencies import validate_image, validate_images
from apps.products.models import Product
from apps.products.schemas import (
    NewCategory,
    OrderSchema,
    PaginatorSavedCategoryResponseSchema,
    PaginatorSavedProductResponseSchema,
    PatchCategorySchema,
    SavedCategorySchema,
    SavedProductSchema,
)
from apps.users.constants import UserPermissionsEnum
from apps.users.models import User
from fastapi import APIRouter, Depends, Form, HTTPException, Path, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from storage.s3 import s3_storage

router_categories = APIRouter()
router_products = APIRouter()
router_orders = APIRouter()


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


@router_categories.get("/{id}")
async def get_category_by_id(
    category_id: int = Path(..., description="The id of the item", ge=1, alias="id"),
    session: AsyncSession = Depends(get_async_session),
) -> SavedCategorySchema:
    saved_category = await category_manager.get(
        session=session, field=Category.id, field_value=category_id
    )
    if not saved_category:
        raise HTTPException(
            detail="Category with this id not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return saved_category


@router_categories.get("/")
async def get_categories(
    params: Annotated[SearchParamsSchema, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> PaginatorSavedCategoryResponseSchema:
    result = await category_manager.get_items_paginated(
        session=session,
        params=params,
        targeted_schema=SavedCategorySchema,
        search_fields=[Category.name],
    )
    return result


@router_categories.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permissions([UserPermissionsEnum.CAN_CREATE_CATEGORY]))
    ],
)
async def update_category(
    patch_data: PatchCategorySchema,
    category_id: int = Path(..., description="The id of the item", ge=1, alias="id"),
    session: AsyncSession = Depends(get_async_session),
) -> SavedCategorySchema:
    updated_category = await category_manager.patch(
        session=session, instance_id=category_id, data_to_patch=patch_data
    )
    return updated_category


@router_categories.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permissions([UserPermissionsEnum.CAN_CREATE_CATEGORY]))
    ],
)
async def delete_category(
    category_id: int = Path(..., description="The id of the item", ge=1, alias="id"),
    session: AsyncSession = Depends(get_async_session),
):
    await category_manager.delete_item(session=session, instance_id=category_id)


@router_products.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(require_permissions([UserPermissionsEnum.CAN_CREATE_PRODUCT]))
    ],
)
async def create_product(
    title: str = Form(min_length=3, max_length=200),
    description: str = Form(min_length=3, max_length=2048),
    price: float = Form(ge=0.01),
    category_id: int = Form(gt=0),
    main_image: UploadFile = Depends(validate_image),
    images: list[UploadFile] | None = Depends(validate_images),
    session: AsyncSession = Depends(get_async_session),
) -> SavedProductSchema:
    is_category_exists = await category_manager.item_exists(
        field=Category.id, field_value=category_id, session=session
    )
    if not is_category_exists:
        raise HTTPException(
            detail="Category with this id not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    is_product_exists = await product_manager.item_exists(
        field=Product.title, field_value=title, session=session
    )
    if is_product_exists:
        raise HTTPException(
            detail="Product with this title already exists",
            status_code=status.HTTP_409_CONFLICT,
        )

    product_uuid = uuid.uuid4()

    files: list[UploadFile] = []

    if main_image is not None:
        files.append(main_image)

    if images:
        files.extend(images)

    main_image_url = None
    images_urls: list[str] = []

    if files:
        try:
            uploaded_urls = await s3_storage.upload_files(
                files=files,
                uuid_obj=product_uuid,
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
                detail="Failed to upload files to S3",
            )

        if main_image and uploaded_urls:
            main_image_url = uploaded_urls[0]
            images_urls = uploaded_urls[1:]
        else:
            images_urls = uploaded_urls

    created_product = await product_manager.create(
        title=title.strip(),
        description=description.strip(),
        price=price,
        images=images_urls,
        main_image=main_image_url,
        category_id=category_id,
        session=session,
    )
    return SavedProductSchema.model_validate(created_product)


@router_products.get("/{id}")
async def get_product_by_id(
    product_id: int = Path(..., description="The id of the item", ge=1, alias="id"),
    session: AsyncSession = Depends(get_async_session),
) -> SavedProductSchema:
    saved_product = await product_manager.get(
        session=session, field=Product.id, field_value=product_id
    )
    if not saved_product:
        raise HTTPException(
            detail="Product with this id not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return saved_product


@router_products.get("/")
async def get_products(
    params: Annotated[SearchParamsSchema, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> PaginatorSavedProductResponseSchema:
    result = await product_manager.get_items_paginated(
        session=session,
        params=params,
        targeted_schema=SavedProductSchema,
        search_fields=[Product.title, Product.description],
    )
    return result


@router_products.patch(
    "/{id}",
    status_code=status.HTTP_200_OK,
    dependencies=[
        Depends(require_permissions([UserPermissionsEnum.CAN_CREATE_PRODUCT]))
    ],
)
async def update_product(
    patch_data: SavedProductSchema,
    product_id: int = Path(..., description="The id of the item", ge=1, alias="id"),
    session: AsyncSession = Depends(get_async_session),
) -> SavedProductSchema:
    updated_product = await product_manager.patch(
        session=session, instance_id=product_id, data_to_patch=patch_data
    )
    return updated_product


@router_products.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(require_permissions([UserPermissionsEnum.CAN_CREATE_PRODUCT]))
    ],
)
async def delete_product(
    product_id: int = Path(..., description="The id of the item", ge=1, alias="id"),
    session: AsyncSession = Depends(get_async_session),
):
    await product_manager.delete_item(session=session, instance_id=product_id)


@router_orders.get("/")
async def get_current_order(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> OrderSchema:
    order = await order_manager.get_or_create(
        session=session, user_id=user.id, is_closed=False
    )
    return OrderSchema.model_validate(order)
