# backend/app/debug.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import User
from app.database import get_db

router = APIRouter()

@router.post("/debug/users/init")
def seed_users(db: Session = Depends(get_db)):
    users = [
        {"id": 1, "name": "Alice Manager", "email": "alice@company.com", "role": "manager"},
        {"id": 2, "name": "Bob Employee", "email": "bob@company.com", "role": "employee", "manager_id": 1},
        {"id": 3, "name": "Charlie Employee", "email": "charlie@company.com", "role": "employee", "manager_id": 1},
        {"id": 4, "name": "David Employee", "email": "david@company.com", "role": "employee", "manager_id": 1},
        {"id": 5, "name": "Eve Manager", "email": "eve@company.com", "role": "manager"},
        {"id": 6, "name": "Frank Employee", "email": "frank@company.com", "role": "employee", "manager_id": 5},
        {"id": 7, "name": "Grace Employee", "email": "grace@company.com", "role": "employee", "manager_id": 5},
    ]

    created = []
    for u in users:
        if not db.query(User).filter(User.email == u["email"]).first():
            db.add(User(**u))
            created.append(u["email"])

    db.commit()
    return {"created": created}
