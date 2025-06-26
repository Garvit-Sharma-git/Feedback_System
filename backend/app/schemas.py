from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    manager = "manager"
    employee = "employee"

class FeedbackBase(BaseModel):
    employee_id: int
    strengths: str
    improvements: str
    sentiment: str
    is_anonymous: Optional[bool] = False

class FeedbackCreate(FeedbackBase):
    pass

class FeedbackComment(BaseModel):
    comment: str

class FeedbackOut(FeedbackBase):
    id: int
    acknowledged: bool
    manager_id: int
    manager_name: Optional[str]  
    manager_email: Optional[str]  
    employee_comment: Optional[str]

    class Config:
        orm_mode = True
