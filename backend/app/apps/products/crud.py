from apps.core.base_crud import BaseCRUDManager

from .models import Category, Order, Product


class CategoryCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = Category


class ProductCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = Product


class OrderCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = Order


category_manager = CategoryCRUDManager()
product_manager = ProductCRUDManager()
order_manager = OrderCRUDManager()
