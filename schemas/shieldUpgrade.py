import json

from pydantic import BaseModel, Field
from typing import Optional, Dict
import math


class ShieldUpgradeSchema(BaseModel):
    id: int
    shield_name: Optional[str] = Field(..., alias="shield name")
    upgrade: Optional[str]
    attack_power: Optional[Dict[str, str]] = Field(..., alias="attack power")
    stat_scaling: Optional[Dict[str, str]] = Field(..., alias="stat scaling")
    passive_effects: Optional[Dict[str, str]] = Field(..., alias="passive effects")
    damage_reduction: Optional[Dict[str, str]] = Field(..., alias="damage reduction (%)")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True  # Allow alias usage, e.g., "shield name"

    @classmethod
    def sanitize(cls, data):
        """Sanitize data by replacing NaN values with None."""
        for key, value in data.items():
            if isinstance(value, float) and math.isnan(value):
                data[key] = None
            elif key in ["damage reduction (%)", "passive effects", "stat scaling", "attack power"] and isinstance(value, str):
                try:
                    data[key] = json.loads(value.replace("'", '"'))
                except json.JSONDecodeError:
                    data[key] = None
        return data

    def dict(self, **kwargs):
        """Override the dict method to sanitize the data."""
        data = super().dict(**kwargs)
        return self.sanitize(data)
