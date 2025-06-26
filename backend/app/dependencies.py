# backend/app/dependencies.py

from fastapi import Header, HTTPException
from app.auth import get_mocked_user
from typing import Optional

def get_current_user(x_user_email: Optional[str] = Header(None)):
    if not x_user_email:
        raise HTTPException(status_code=400, detail="Missing X-User-Email header")
    user = get_mocked_user(x_user_email)
    return user
