# backend/app/models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class RoleEnum(str, enum.Enum):
    manager = "manager"
    employee = "employee"

class SentimentEnum(str, enum.Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True)
    role = Column(Enum(RoleEnum))
    team_id = Column(Integer, nullable=True)  # optional grouping
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)


# backend/app/models.py

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("users.id"))
    manager_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # manager_id can now be null
    strengths = Column(Text)
    improvements = Column(Text)
    sentiment = Column(Enum(SentimentEnum))
    acknowledged = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    is_anonymous = Column(Boolean, default=False)  # <-- new
    employee_comment = Column(Text, nullable=True)


