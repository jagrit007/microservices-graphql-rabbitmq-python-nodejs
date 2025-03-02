from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from .db import Base

class User(Base):
    __tablename__ = "users"


    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    preferences = Column(PG_ARRAY(String), nullable=False, default=[])

