from pydantic import BaseModel, Field


class IdSchema(BaseModel):
    id: int = Field(description='User id', examples=[1], gt=0)