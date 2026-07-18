from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.auth.auth import hash_password, verify_password, create_access_token, get_current_user
from app.database import get_db
from app.models import User
from app.schemas import UserOut, UserCreate

router = APIRouter(prefix="/users")


@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        or_(
            User.username == user.username,
            User.email == user.email
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Username or email exists"
        )

    password_hash = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=password_hash
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session= Depends(get_db)):

    db_user = db.query(User).filter(User.username == form_data.username).first()

    if not db_user or not verify_password(form_data.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # token = create_access_token({"sub": str(db_user.id)})
    token = create_access_token(
        data= {
            "sub": db_user.username,
            "user_id": str(db_user.id)
        }
    )

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
