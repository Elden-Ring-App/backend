from pydantic import BaseModel, Field
from typing import Optional
import math


class WeaponSchema(BaseModel):
    id: int
    weapon_id: int
    name: str
    image: Optional[str]
    weight: Optional[float]
    description: Optional[str]
    dlc: Optional[int]
    requirements: Optional[str]
    damage_type: Optional[str] = Field(..., alias="damage type")
    category: Optional[str]
    passive_effect: Optional[str] = Field(..., alias="passive effect")
    skill: Optional[str]
    FP_cost: Optional[str] = Field(..., alias="FP cost")

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
