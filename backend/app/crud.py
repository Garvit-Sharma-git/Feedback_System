# backend/app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_team_members(db: Session, manager_id: int):
    return db.query(models.User).filter(models.User.manager_id == manager_id).all()


def create_feedback(db: Session, feedback: schemas.FeedbackCreate, manager_id: int):
    db_feedback = models.Feedback(
        employee_id=feedback.employee_id,
        manager_id=manager_id,
        strengths=feedback.strengths,
        improvements=feedback.improvements,
        sentiment=feedback.sentiment,
        is_anonymous=feedback.is_anonymous,
    )
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback

def get_feedback_for_employee(db: Session, employee_id: int):
    feedbacks = db.query(models.Feedback).filter(models.Feedback.employee_id == employee_id).all()
    result = []
    for f in feedbacks:
        if f.is_anonymous:
            manager_name = None
            manager_email = None
        else:
            manager = db.query(models.User).filter(models.User.id == f.manager_id).first()
            manager_name = manager.name if manager else None
            manager_email = manager.email if manager else None

        result.append({
            "id": f.id,
            "employee_id": f.employee_id,
            "manager_id": f.manager_id,
            "manager_name": manager_name,
            "manager_email": manager_email,
            "strengths": f.strengths,
            "improvements": f.improvements,
            "sentiment": f.sentiment,
            "acknowledged": f.acknowledged,
            "is_anonymous": f.is_anonymous,
            "created_at": f.created_at,
            "updated_at": f.updated_at
        })
    return result




def acknowledge_feedback(db: Session, feedback_id: int):
    feedback = db.query(models.Feedback).filter(models.Feedback.id == feedback_id).first()
    
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")

    feedback.acknowledged = True
    db.commit()
    db.refresh(feedback)
    return feedback


# crud.py

def get_feedback_given_by_manager(db: Session, manager_id: int):
    feedbacks = db.query(models.Feedback).filter(models.Feedback.manager_id == manager_id).all()
    result = []
    for f in feedbacks:
        employee = db.query(models.User).filter(models.User.id == f.employee_id).first()
        result.append({
            "id": f.id,
            "employee_id": f.employee_id,
            "employee_name": employee.name if employee else None,
            "employee_email": employee.email if employee else None,
            "manager_id": f.manager_id,
            "strengths": f.strengths,
            "improvements": f.improvements,
            "sentiment": f.sentiment,
            "acknowledged": f.acknowledged,
            "created_at": f.created_at,
            "updated_at": f.updated_at,
            "employee_comment": f.employee_comment,
        })
    return result

