
from sqlalchemy.orm import Mapped, mapped_column

from apps.core.base_models import Base


class User(Base):
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]


