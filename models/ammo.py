from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional
import math


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None, config=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


class AmmoModel(BaseModel):
    id: int
    name: str
    image: Optional[str]
    type: Optional[str]
    damage_type: Optional[str] = Field(..., alias="damage type")
    attack_power: Optional[str] = Field(..., alias="attack power")
    passive_effect: Optional[str] = Field(..., alias="passive effect")
    description: Optional[str]
    dlc: Optional[int]
    mongo_id: PyObjectId = Field(alias="_id")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }
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
