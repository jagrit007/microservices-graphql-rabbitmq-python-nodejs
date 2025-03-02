from sqlalchemy.orm import Session
from .models import User
from .schemas import UserCreate, UserUpdate
from typing import Optional

def create_user(db: Session, user: UserCreate, hashed_password: str) -> User:
    #TODO: check user exists
    print(hashed_password)
    db_user = User(
                    email=user.email,
                    name=user.name,
                    password=hashed_password,
                    preferences=user.preferences
                    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def update_user_preferences(db: Session, user_id: int, updateVals: UserUpdate) -> Optional[User]:
    db_user = get_user_by_id(db, user_id)

    if db_user:
        db_user.preferences = updateVals.preferences

        if updateVals.name:
            db_user.name = updateVals.name

        if updateVals.email:
            db_user.email = updateVals.email

        db.commit()
        db.refresh(db_user)

    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = get_user_by_id(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False