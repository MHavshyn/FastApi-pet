from fastapi import File, HTTPException, UploadFile, status

ALLOWED_IMAGE_FILE_TYPES = {"image/jpeg", "image/png", "image/gif"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB


async def validate_image(image: UploadFile = File(...)) -> UploadFile:
    if image.content_type not in ALLOWED_IMAGE_FILE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid file type"
        )

    file_size = len(await image.read())
    await image.seek(0)
    if file_size > MAX_IMAGE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Image too large"
        )

    return image


async def validate_images(
    image: list[UploadFile] = File(default=None, max_length=10),
) -> list[UploadFile]:
    if image is None:
        return []

    if len(image) > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Too many images"
        )

    for img in image:
        await validate_image(img)

    return image
