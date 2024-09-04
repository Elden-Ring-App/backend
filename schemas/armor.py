import json

from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import math


class ArmorSchema(BaseModel):
    id: int
    name: str
    image: Optional[str]
    description: Optional[str]
    type: Optional[str]
    damage_negation: Optional[List[Dict[str, str]]] = Field(..., alias="damage negation")
    resistance: Optional[List[Dict[str, str]]]
    weight: Optional[float]
    special_effect: Optional[str] = Field(..., alias="special effect")
    how_to_acquire: Optional[str] = Field(..., alias="how to acquire")
    in_game_section: Optional[str] = Field(..., alias="in-game section")
    dlc: Optional[str]

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True  # Allow field aliases to map API data to internal schema field names

    @classmethod
    def sanitize(cls, data):
        """Sanitize the data by replacing NaN values with None."""
        for key, value in data.items():
            if isinstance(value, float) and math.isnan(value):
                data[key] = None
            elif key in ["damage negation", "resistance"] and isinstance(value, str):
                try:
                    data[key] = json.loads(value.replace("'", '"'))
                except json.JSONDecodeError:
                    data[key] = None
        return data

    def dict(self, **kwargs):
        """Override the dict method to sanitize the data."""
        data = super().dict(**kwargs)
        return self.sanitize(data)
