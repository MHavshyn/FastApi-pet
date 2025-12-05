import logging
from typing import NoReturn

import sentry_sdk
from fastapi import HTTPException, status
from sentry_sdk import capture_message
from sentry_sdk.integrations.logging import LoggingIntegration
from settings import settings


def unexpected_error(
    log_message: str, user_message: str = "General error. Call support"
) -> NoReturn:
    capture_message(log_message, level="error")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=user_message)


def init_sentry():
    sentry_logging = LoggingIntegration(
        event_level=logging.ERROR,
    )

    sentry_sdk.init(
        dsn=settings.SENTRY_DNS, send_default_pii=True, integrations=[sentry_logging]
    )
