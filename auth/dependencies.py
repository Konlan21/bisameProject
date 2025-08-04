from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth.jwt_handler import SECRET_KEY, ALGORITHM
from db.fake_db import users_db
from auth.models import User

security = HTTPBearer()

def get_current_user(token: HTTPAuthorizationCredentials = Depends(security)) -> User:
    print("Received raw token:", token.credentials)  # DEBUG

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        print("Decoded payload:", payload)  # DEBUGING

        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token missing username")

        user = users_db.get(username)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        if not user.is_active or user.is_banned:
            raise HTTPException(status_code=403, detail="Inactive or banned user")

        return user

    except JWTError as e:
        print("JWT Decode Error:", str(e))  # <---- IMPORTANT
        raise HTTPException(status_code=401, detail="Invalid token")
