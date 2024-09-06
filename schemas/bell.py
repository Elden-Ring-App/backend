from pydantic import BaseModel, model_validator
from typing import Optional
import math


class BellSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    type: Optional[str]
    effect: Optional[str]
    description: Optional[str]
    dlc: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True  # Allow field aliases to map API data to internal schema field names

    @classmethod
    def sanitize(cls, data):
        """Sanitize the data by replacing NaN values with None."""
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
        """Override the dict method to sanitize the data."""
        data = super().dict(**kwargs)
        return self.sanitize(data)
