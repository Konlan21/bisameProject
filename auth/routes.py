# auth/routes.py
from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from db.fake_db import users_db
from auth.jwt_handler import create_access_token, create_refresh_token
from fastapi import Depends
from fastapi import Request, HTTPException
from jose import JWTError, jwt
from auth.jwt_handler import create_access_token
from db.fake_db import users_db
from auth.jwt_handler import SECRET_KEY, ALGORITHM
from main import limiter
from auth.models import RefreshTokenRequest

router = APIRouter() 

@router.post("/login")
@limiter.limit("5/minute")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_active or user.is_banned:
        raise HTTPException(status_code=403, detail="Inactive or banned user")
    
    access_token = create_access_token(data={"sub": user.username, "role": user.role})
    refresh_token = create_refresh_token(data={"sub": user.username})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "role": user.role
    }





@router.post("/refresh")
@limiter.limit("10/minute")
def refresh_token(data: RefreshTokenRequest):
    try:
        refresh_token = data.refresh_token

        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if not username or username not in users_db:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = users_db[username]
        if not user.is_active or user.is_banned:
            raise HTTPException(status_code=403, detail="User inactive or banned")

        new_access_token = create_access_token(data={"sub": user.username, "role": user.role})

        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
