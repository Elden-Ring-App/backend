from pydantic import BaseModel, model_validator
from typing import Optional
import math


class SkillSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    type: Optional[str]
    equipament: Optional[str]
    charge: Optional[str]
    FP: Optional[str]
    effect: Optional[str]
    locations: Optional[str]
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
