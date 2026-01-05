from datetime import datetime
from enum import StrEnum

from apps.core.schemas import IdSchema, InstanceVersion, PaginationResponseSchema
from pydantic import BaseModel, ConfigDict, Field


class NewCategory(BaseModel):
    name: str = Field(min_length=3, max_length=50, examples=["Laptops", "books"])

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


class SavedCategorySchema(NewCategory, IdSchema, InstanceVersion):
    class Config:
        from_attributes = True


class PaginatorSavedCategoryResponseSchema(PaginationResponseSchema):
    items: list[SavedCategorySchema]


class PatchCategorySchema(InstanceVersion, NewCategory):
    pass


class SavedProductSchema(IdSchema):
    title: str
    description: str
    price: float
    category_id: int
    main_image: str
    images: list[str]

    class Config:
        from_attributes = True


class PaginatorSavedProductResponseSchema(PaginationResponseSchema):
    items: list[SavedCategorySchema]


class OrderProductsSchema(BaseModel):
    price: float
    quantity: int
    total: float
    product: SavedProductSchema

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    created_at: datetime = Field(examples=[datetime.now()])
    is_closed: bool = Field(examples=[False])
    user_id: int
    cost: float
    products: list[OrderProductsSchema]

    class Config:
        from_attributes = True


class ModeChangeOrderProductQuantityEnum(StrEnum):
    INCREASE = "increase"
    DECREASE = "decrease"
    SET = "set"
