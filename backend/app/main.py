from fastapi import FastAPI, Depends, HTTPException
from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import SessionLocal, Base, engine
from app.models import User
from . import database, models, schemas, crud, auth
from app.dependencies import get_current_user
from sqlalchemy import text
from app.debug import router as debug_router 

from fastapi.responses import FileResponse
from xhtml2pdf import pisa
from io import BytesIO
import os
from fastapi import Response



current_user: dict = Depends(get_current_user)


# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Allow local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://feedback-system-cyan.vercel.app"],  # exact frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(debug_router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Login endpoint
class LoginRequest(BaseModel):
    email: str
    role: str
    
@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email, User.role == data.role).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role
    }


# @app.post("/auth/login")
# def login(data: LoginRequest):
#     return auth.get_mocked_user(data.email)

# Get team members
@app.get("/team")
def get_team(
    manager_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager" or current_user["id"] != manager_id:
        raise HTTPException(status_code=403, detail="Unauthorized to view this team")
    return crud.get_team_members(db, manager_id)


# Get feedback for an employee
@app.get("/feedback/{employee_id}")
def get_feedback_for_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] == "employee" and current_user["id"] != employee_id:
        raise HTTPException(status_code=403, detail="Employees can only view their own feedback")
    return crud.get_feedback_for_employee(db, employee_id)


# Get feedback given by a manager
@app.get("/feedback/manager/{manager_id}")
def get_feedback_given(
    manager_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager" or current_user["id"] != manager_id:
        raise HTTPException(status_code=403, detail="Unauthorized to view feedback")

    return crud.get_feedback_given_by_manager(db, manager_id)





# Create new feedback
@app.post("/feedback")
def create_feedback(
    feedback: schemas.FeedbackCreate,
    manager_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "manager" or current_user["id"] != manager_id:
        raise HTTPException(status_code=403, detail="Only the manager can submit feedback")
    return crud.create_feedback(db, feedback, manager_id)

@app.get("/debug/users")
def debug_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Acknowledge feedback
@app.post("/feedback/{feedback_id}/acknowledge")
def acknowledge(
    feedback_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    try:
        feedbacks = crud.get_feedback_for_employee(db, current_user["id"])

        
        if not any(f["id"] == feedback_id for f in feedbacks):
            raise HTTPException(status_code=404, detail="Feedback not found for this user")

        crud.acknowledge_feedback(db, feedback_id)
        return {"success": True}
    except Exception as e:
        print(f"[ERROR] Failed to acknowledge feedback: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.post("/feedback/{feedback_id}/comment")
def submit_feedback_comment(
    feedback_id: int,
    comment_data: schemas.FeedbackComment,
    db: Session = Depends(get_db),
):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    
    feedback.employee_comment = comment_data.comment
    db.commit()
    db.refresh(feedback)
    return {"message": "Comment added"}



from app.models import Feedback, SentimentEnum

from fastapi import status
from sqlalchemy.exc import SQLAlchemyError

@app.get("/debug/find-invalid-sentiments")
def find_invalid_sentiments(db: Session = Depends(get_db)):
    try:
        allowed_values = {s.value for s in SentimentEnum}
        print(f"Allowed sentiment values: {allowed_values}")
        all_feedbacks = db.query(Feedback).all()
        print(f"Total feedback records: {len(all_feedbacks)}")
        invalid = [f for f in all_feedbacks if f.sentiment not in allowed_values]
        return [{"id": f.id, "sentiment": f.sentiment} for f in invalid]
    except SQLAlchemyError as e:
        print(f"[ERROR] SQLAlchemy exception: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="DB error")


from sqlalchemy import text

from sqlalchemy import text
from fastapi import HTTPException

@app.post("/debug/fix-invalid-sentiments")
def fix_invalid_sentiments_raw():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT id, sentiment FROM feedbacks"))
            rows = result.fetchall()

            valid_sentiments = {"positive", "neutral", "negative"}
            to_fix = []

            for row in rows:
                fid, sentiment = row  # FIXED here
                if sentiment not in valid_sentiments:
                    print(f"Invalid sentiment '{sentiment}' found in feedback ID {fid}")
                    to_fix.append(fid)

            for fid in to_fix:
                connection.execute(
                    text("UPDATE feedbacks SET sentiment = :s WHERE id = :i"),
                    {"s": "neutral", "i": fid}
                )

            connection.commit()

        return {"status": "ok", "fixed_ids": to_fix}
    except Exception as e:
        print(f"Error in fix_invalid_sentiments: {e}")
        raise HTTPException(status_code=500, detail=str(e))



@app.get("/feedback/manager/{manager_id}/export/pdf")
def export_feedback_pdf(manager_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "manager" or current_user["id"] != manager_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    feedbacks = crud.get_feedback_given_by_manager(db, manager_id)

    html_content = "<h1>Feedback Summary</h1>"
    for f in feedbacks:
        html_content += f"""
            <div style="margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px;">
                <strong>Employee:</strong> {f['employee_name'] or 'Anonymous'}<br>
                <strong>Sentiment:</strong> {f['sentiment'].capitalize()}<br>
                <strong>Strengths:</strong><br>{f['strengths']}<br>
                <strong>Improvements:</strong><br>{f['improvements']}<br>
                <strong>Employee Comment:</strong><br>{f['employee_comment'] or 'N/A'}<br>
                <small>Created At: {f['created_at']}</small><br>
            </div>
        """

    # Convert to PDF
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf)

    if pisa_status.err:
        raise HTTPException(status_code=500, detail="Error generating PDF")

    pdf.seek(0)
    return Response(pdf.read(), media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename=feedback_manager_{manager_id}.pdf"
    })







# Get all users (for debugging)
@app.get("/debug/users")
def debug_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Seed initial mock data on startup
@app.on_event("startup")
def seed_data():
    db = SessionLocal()
    from .schemas import RoleEnum

    if db.query(User).first():
        return

    print("[Seed] Seeding mock users...")
    alice = User(name="Alice Manager", email="alice@company.com", role=RoleEnum.manager)
    db.add(alice)
    db.commit()
    db.refresh(alice)

    bob = User(name="Bob Employee", email="bob@company.com", role=RoleEnum.employee, manager_id=alice.id)
    db.add(bob)
    db.commit()
    db.close()
    print("[Seed] Done.")
