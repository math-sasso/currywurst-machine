from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime


# Define the model for messages
class Transactions(Base):
    """Transactions Table

    Args:
        Base (_type_): Base SQL Alchemy table
    """
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)