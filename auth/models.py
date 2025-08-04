from pydantic import BaseModel
from typing import Optional, Literal


class User(BaseModel):
    username: str
    password: str
    role: Literal["customer", "vendor", "admin", "staff"]
    is_active: bool = True
    is_banned: bool = False
    


# auth/models.py
from pydantic import BaseModel

class RefreshTokenRequest(BaseModel):
    refresh_token: str

