from pydantic import BaseModel, EmailStr
from typing import Optional, List, Union


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    preferences: List[str]

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    preferences: List[str]

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    # Allow the user to be able to change name and email as well
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    preferences: Optional[List[str]] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str