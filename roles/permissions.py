# roles/permissions.py
from fastapi import Depends, HTTPException
from auth.dependencies import get_current_user
from auth.models import User

def require_role(required_role: str):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker
