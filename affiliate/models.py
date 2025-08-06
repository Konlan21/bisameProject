from typing import Optional, List
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


class AffiliateLink(BaseModel):
    user_id: PyObjectId = Field(..., alias="user_id")
    referred_by: Optional[PyObjectId] = Field(None, alias="referred_by")


class Order(BaseModel):
    user_id: PyObjectId
    amount: float


class Commission(BaseModel):
    user_id: PyObjectId
    order_id: PyObjectId
    level: str
    amount: float
    date: str


class PromotionPackage(BaseModel):
    name: str
    price: float
    features: List[str]
    discount_rate: float
