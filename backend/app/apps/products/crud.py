from apps.core.base_crud import BaseCRUDManager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Category, Order, OrderProduct, Product


class CategoryCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = Category


class ProductCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = Product


class OrderCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = Order

    async def get_order_with_products(
        self, session: AsyncSession, order_id: int
    ) -> Order:
        result = await session.execute(
            select(self.model)
            .options(
                selectinload(self.model.products).selectinload(OrderProduct.product)
            )
            .filter(self.model.id == order_id)
        )
        order = result.scalars().first()
        if order.products:
            order.products = [p for p in order.products if p.quantity]

        return order


class OrderProductCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = OrderProduct

    async def change_quantity_and_set_current_price(
        self,
        session: AsyncSession,
        order: Order,
        product: Product,
        quantity: int,
        is_set_quantity_mode: bool,
    ) -> None:
        order_product: OrderProduct | None = await self.get_or_create(
            session=session,
            order_id=order.id,
            product_id=product.id,
        )
        if is_set_quantity_mode:
            order_product.quantity = quantity
        else:
            order_product.quantity += quantity
            if order_product.quantity < 0:
                order_product.quantity = 0

        order_product.current_price = product.price
        session.add(order_product)
        await session.commit()
        await session.refresh(order_product)
        await session.refresh(order)


category_manager = CategoryCRUDManager()
product_manager = ProductCRUDManager()
order_manager = OrderCRUDManager()
order_product_manager = OrderProductCRUDManager()
