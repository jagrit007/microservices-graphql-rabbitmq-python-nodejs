from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class Recommendation(BaseModel):
    id: Optional[str] = Field(alias="_id")
    user_id: int
    products: List[str]  # List of recommended product IDs
    created_at: datetime = Field(default_factory=datetime.utcnow)
