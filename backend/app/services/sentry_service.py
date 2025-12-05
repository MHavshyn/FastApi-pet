from typing import NoReturn

from fastapi import HTTPException, status
from sentry_sdk import capture_message


def unexpected_error(
    log_message: str, user_message: str = "General error. Call support"
) -> NoReturn:
    capture_message(log_message, level="error")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=user_message)
