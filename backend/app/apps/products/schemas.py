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
