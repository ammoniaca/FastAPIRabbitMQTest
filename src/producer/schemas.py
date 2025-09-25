
from pydantic import BaseModel, Field
from datetime import datetime


class PayloadModel(BaseModel):
    queue_name: str = Field(...)
    process_name: str = Field(...)
    random_string: str = Field(...)
    created_at: datetime = Field(...)

