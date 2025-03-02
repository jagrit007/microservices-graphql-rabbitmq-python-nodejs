from typing import Optional, Union
from pydantic import BaseModel, Field
from bson import ObjectId
from datetime import datetime

class PyObjectId(str):
    """Custom ObjectId type to handle MongoDB _id serialization"""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str) and ObjectId.is_valid(v):
            return v
        raise ValueError("Invalid ObjectId")

class Notification(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: int = Field(...)
    type: str = Field(...)
    content: Union[str, dict] = Field(...)
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    read: bool = Field(default=False)

    model_config = {
        "json_encoders": {ObjectId: str},
        "populate_by_name": True,
        "from_attributes": True,
        "arbitrary_types_allowed": True,
    }
