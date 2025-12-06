from apps.core.base_models import Base
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=True)
