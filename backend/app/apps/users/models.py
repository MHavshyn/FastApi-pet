from apps.core.base_models import Base
from sqlalchemy import String, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from .constants import UserPermissionsEnum


class User(Base):
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=True)
    permissions: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        default=lambda: [UserPermissionsEnum.CAN_SEE_USERS],
        nullable=False,
        server_default=text("'{CAN_SELF_DELETE}'::text[]"),
    )
