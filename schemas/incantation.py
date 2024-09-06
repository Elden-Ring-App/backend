from pydantic import BaseModel, Field, model_validator
from typing import Optional
import math


class IncantationSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    description: Optional[str]
    effect: Optional[str]
    FP: Optional[str]
    slot: Optional[int]
    INT: Optional[int]
    FAI: Optional[int]
    ARC: Optional[int]
    stamina_cost: Optional[int] = Field(..., alias="stamina cost")
    bonus: Optional[str]
    group: Optional[str]
    location: Optional[str]
    dlc: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

    @classmethod
    def sanitize(cls, data):
        for key, value in data.items():
            if isinstance(value, float) and math.isnan(value):
                data[key] = None
        return data

    @model_validator(mode="before")
    @classmethod
    def sanitize_data(cls, values):
        """Apply to sanitize before validation."""
        sanitized_values = cls.sanitize(values)
        return sanitized_values

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        return self.sanitize(data)
