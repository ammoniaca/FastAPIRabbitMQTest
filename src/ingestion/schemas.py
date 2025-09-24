from pydantic import BaseModel, Field, model_validator


class IntRanges(BaseModel):
    min: int
    max: int

    @model_validator(mode="after")
    def check_min_max(self):
        if self.min > self.max:
            raise ValueError(f"min ({self.min}) cannot be greater than max ({self.max})")
        return self

class RequestModel(BaseModel):
    queue_name: str = Field(...)
    process_tag: str = Field(...)
    range: IntRanges = Field(...)

    def __getitem__(self, item):
        return getattr(self, item)
