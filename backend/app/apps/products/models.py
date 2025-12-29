from apps.core.base_models import Base, UpdatedAtMixin, UUIDMixin
from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Category(UpdatedAtMixin, Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(70), unique=True, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    products = relationship("Product", back_populates="category")

    def __str__(self) -> str:
        return f"<Category {self.name} - #{self.version}>"


class Product(UpdatedAtMixin, UUIDMixin, Base):
    title: Mapped[str] = mapped_column(String(70), nullable=False)
    description: Mapped[str] = mapped_column(String(2048), default="")
    price: Mapped[float] = mapped_column(nullable=False)
    main_image: Mapped[int] = mapped_column(Integer, nullable=False)
    images: Mapped[list[str]] = mapped_column(ARRAY(String), default=list)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False
    )

    category = relationship("Category", back_populates="products")

    def __str__(self) -> str:
        return f"<Product {self.title} - #{self.id}, current price {self.price}>"


class Order(UpdatedAtMixin, UUIDMixin, Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_closed: Mapped[bool] = mapped_column(default=False)
    user = relationship("User", back_populates="orders")
    products = relationship("OrderProduct", back_populates="order", lazy="selectin")

    @property
    def cost(self) -> float:
        return sum([product.total for product in self.products])


class OrderProduct(UpdatedAtMixin, Base):
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    price: Mapped[float] = mapped_column(default=0.0)
    quantity: Mapped[int] = mapped_column(default=0)

    order = relationship("Order", back_populates="products", lazy="selectin")

    __table_args__ = (
        UniqueConstraint("order_id", "product_id", name="uq_order_product"),
    )

    @property
    def total(self) -> float:
        return self.price * self.quantity
