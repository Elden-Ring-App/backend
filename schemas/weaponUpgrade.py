from pydantic import BaseModel, Field
from typing import Optional
import math


class WeaponUpgradeSchema(BaseModel):
    id: int
    weapon_name: Optional[str] = Field(..., alias="weapon name")
    upgrade: Optional[str]
    attack_power: Optional[str] = Field(..., alias="attack power")
    stat_scaling: Optional[str] = Field(..., alias="stat scaling")
    passive_effects: Optional[str] = Field(..., alias="passive effects")
    damage_reduction: Optional[str] = Field(..., alias="damage reduction (%)")

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
