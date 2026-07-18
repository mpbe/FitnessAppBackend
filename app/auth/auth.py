from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from app.config import config
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

password_hasher = CryptContext(schemes="bcrypt", deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


def hash_password(password: str):
    return password_hasher.hash(password)


def verify_password(password: str, hashed_password: str):
    return password_hasher.verify(password, hashed_password)


def create_access_token(data: dict):
    data_to_encode = data.copy()

    expiry_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    data_to_encode.update({"exp": expiry_time})

    return jwt.encode(data_to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):

    try:
        # what decode does:
        # verifies token signature
        # checks expiry
        # returns payload dict
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    #equiv SQL is SELECT * FROM users WHERE id = 1;
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user