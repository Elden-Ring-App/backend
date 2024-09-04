from pydantic import BaseModel, Field
from typing import Optional
import math


class SpiritAshSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    type: Optional[str]
    FP_cost: Optional[str] = Field(..., alias="FP cost")
    HP_cost: Optional[int] = Field(..., alias="HP cost")
    effect: Optional[str]
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
        return data

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        return self.sanitize(data)
