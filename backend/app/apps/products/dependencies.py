import re

from apps.auth.dependencies import get_current_user
from apps.core.dependencies import get_async_session
from apps.products.crud import order_manager, product_manager
from apps.products.models import Order, Product
from apps.users.models import User
from fastapi import Body, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

ALLOWED_IMAGE_FILE_TYPES = {"image/jpeg", "image/png", "image/gif"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB

FILENAME_REGEX = re.compile(r"^[A-Za-z0-9_.-]+\.(jpg|jpeg|png|gif)$", re.IGNORECASE)


async def validate_image(image: UploadFile = File(...)) -> UploadFile:
    if image.content_type not in ALLOWED_IMAGE_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type"
        )
    if not image.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    if not FILENAME_REGEX.match(image.filename):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename must contain only English letters, numbers, dots, dashes or underscores",
        )

    file_size = len(await image.read())
    await image.seek(0)
    if file_size > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Image too large"
        )

    return image


async def validate_images(
    images: list[UploadFile] | None = File(default=None, max_length=10),
) -> list[UploadFile] | None:
    if images is None:
        return []

    if len(images) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Too many images"
        )

    for img in images:
        await validate_image(img)

    return images


async def get_order(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
) -> Order:
    return await order_manager.get_or_create(
        session=session, user_id=user.id, is_closed=False
    )


async def get_product(
    product_id: int = Body(ge=1),
    session: AsyncSession = Depends(get_async_session),
) -> Product:
    product = await product_manager.get(
        session=session, field=Product.id, field_value=product_id
    )
    if not product:
        raise HTTPException(
            detail="Product with this id not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return product
