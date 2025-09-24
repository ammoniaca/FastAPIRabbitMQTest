from pydantic import BaseModel, Field


class Items(BaseModel):
    queue: str = Field(...)
    service: str = Field(...)
    number: int = Field(...)
