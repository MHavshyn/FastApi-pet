from apps.core.base_crud import BaseCRUDManager

from .models import Category, Product


class CategoryCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = Category


class ProductCRUDManager(BaseCRUDManager):
    def __init__(self):
        self.model = Product


category_manager = CategoryCRUDManager()
product_manager = ProductCRUDManager()
