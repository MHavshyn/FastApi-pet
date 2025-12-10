from pydantic import BaseModel, Field


class IdSchema(BaseModel):
    id: int = Field(description="User id", examples=[1], gt=0)


class InstanceVersion(BaseModel):
    version: int = Field(description="Version of the instance", examples=[1, 22], gt=0)
