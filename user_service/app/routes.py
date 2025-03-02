from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Depends, Response, status

from .auth import create_access_token, get_current_user
from .schemas import (UserCreate, UserResponse, UserUpdate, Token, UserLogin)
from sqlalchemy.orm import Session
from .crud import create_user, get_user_by_id, get_user_by_email, update_user_preferences
from .db import DatabaseManager
from .utils import hash_password, verify_password
from .models import User

db_manager = DatabaseManager()

user_router = APIRouter()

@user_router.post("/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(db_manager.get_db)):
    existing_user = get_user_by_email(db, email=str(user.email))

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash Password
    hashed_password = hash_password(user.password)
    new_user = create_user(db=db, user=user, hashed_password=hashed_password)

    return new_user

@user_router.post("/login", response_model=Token, status_code=HTTPStatus.OK)
def login(user_credentials: UserLogin, db: Session = Depends(db_manager.get_db)):
    user = get_user_by_email(db, email=str(user_credentials.email))
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@user_router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(db_manager.get_db), current_user: User = Depends(get_current_user)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    return current_user

@user_router.put("/{user_id}", response_model=UserResponse)
def update_preferences(user_id: int, preferences: UserUpdate, db: Session = Depends(db_manager.get_db), current_user: User = Depends(get_current_user)):
    updated_user = update_user_preferences(db, user_id, preferences)

    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")

    return updated_user

@user_router.delete("/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(db_manager.get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return Response(status_code=HTTPStatus.NO_CONTENT, content="User deleted successfully")