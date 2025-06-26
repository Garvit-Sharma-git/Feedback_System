# backend/app/auth.py

from fastapi import HTTPException

# Static mocked users
MOCKED_USERS = [
    {"id": 1, "name": "Alice Manager", "email": "alice@company.com", "role": "manager"},
    {"id": 2, "name": "Bob Employee", "email": "bob@company.com", "role": "employee", "team_id": 1},
    {"id": 3, "name": "Charlie Employee", "email": "charlie@company.com", "role": "employee", "team_id": 1},
    {"id": 4, "name": "David Employee", "email": "david@company.com", "role": "employee", "team_id": 1},
    
    {"id": 5, "name": "Eve Manager", "email": "eve@company.com", "role": "manager"},
    {"id": 6, "name": "Frank Employee", "email": "frank@company.com", "role": "employee", "team_id": 5},
    {"id": 7, "name": "Grace Employee", "email": "grace@company.com", "role": "employee", "team_id": 5},
]


def get_mocked_user(email: str):
    print(f"[DEBUG] Attempting login for: {email}")
    for user in MOCKED_USERS:
        if user["email"] == email:
            return user
    raise HTTPException(status_code=404, detail="User not found")
