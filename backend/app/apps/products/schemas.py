from apps.core.schemas import IdSchema, InstanceVersion
from pydantic import BaseModel, ConfigDict, Field


class NewCategory(BaseModel):
    name: str = Field(min_length=3, max_length=50, examples=["Laptops", "books"])

    model_config = ConfigDict(
        str_strip_whitespace=True,
        extra="forbid",
    )


class SavedCategorySchema(NewCategory, IdSchema, InstanceVersion):
    pass
