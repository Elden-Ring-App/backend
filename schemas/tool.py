from pydantic import BaseModel
from typing import Optional
import math


class ToolSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    description: Optional[str]
    type: Optional[str]
    usage: Optional[str]
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

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        return self.sanitize(data)
