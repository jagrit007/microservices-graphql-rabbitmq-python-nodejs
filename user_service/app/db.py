import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/users.db")



class DatabaseManager:
    def __init__(self, database_url=DATABASE_URL):
        self.engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
        )
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)


    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def init_db(self):
        """
        Initializes the database by creating all tables.
        Useful for setting up the database in development.
        """
        Base.metadata.create_all(bind=self.engine)

    def drop_db(self):
        """
        Drops all tables in the database.
        Useful for resetting the database during testing.
        """
        Base.metadata.drop_all(bind=self.engine)
