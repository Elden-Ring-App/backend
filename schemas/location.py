import json

from pydantic import BaseModel
from typing import Optional, List
import math


class LocationSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    region: Optional[str]
    items: Optional[List[str]]
    npcs: Optional[List[str]]
    creatures: Optional[List[str]]
    bosses: Optional[List[str]]
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
            elif key in ["items", "npcs", "creatures", "bosses"] and isinstance(value, str):
                try:
                    data[key] = json.loads(value.replace("'", '"'))
                except json.JSONDecodeError:
                    data[key] = None
        return data

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        return self.sanitize(data)
