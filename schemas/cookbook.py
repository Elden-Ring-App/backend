import json

from pydantic import BaseModel, Field
from typing import Optional, List
import math


class CookbookSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    effect: Optional[str]
    required_for: Optional[List[str]] = Field(..., alias="required for")
    description: Optional[str]
    dlc: Optional[int]

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True

    @classmethod
    def sanitize(cls, data):
        for key, value in data.items():
            if isinstance(value, float) and math.isnan(value):
                data[key] = None
            elif key in ["required for"] and isinstance(value, str):
                try:
                    data[key] = json.loads(value.replace("'", '"'))
                except json.JSONDecodeError:
                    data[key] = None
        return data

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        return self.sanitize(data)
