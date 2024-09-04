from pydantic import BaseModel, Field
from typing import Optional
import math


class GreatRuneSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    type: Optional[str]
    description: Optional[str]
    effect: Optional[str]
    boss: Optional[str]
    location: Optional[str]
    divine_tower_locations: Optional[str] = Field(..., alias="divine tower locations")
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
