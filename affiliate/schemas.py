from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime




class PlaceOrderRequest(BaseModel):
    vendor_username: str
    amount: float


class UserModel(BaseModel):
    username: str
    email: str
    role: str = "customer" 
    referred_by: Optional[str] = None

class OrderModel(BaseModel):
    user: str 
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class AffiliateCommissionModel(BaseModel):
    user: str 
    referred_user: str
    order_id: str
    level: str
    amount: float
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PromotionPackageModel(BaseModel):
    name: str
    price: float
    discount_percentage: float

class CommissionUsageModel(BaseModel):
    user: str
    amount_used: float
    package_name: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
