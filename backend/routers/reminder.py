from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas import reminder as schemas
from services import reminder_service
from database import SessionLocal

router = APIRouter(prefix="/reminders", tags=["reminders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Reminder)
def create_reminder(reminder: schemas.ReminderCreate, db: Session = Depends(get_db)):
    return reminder_service.create_reminder(db, reminder)


@router.get("/user/{user_id}", response_model=list[schemas.Reminder])
def read_reminders(user_id: int, db: Session = Depends(get_db)):
    return reminder_service.get_reminders(db, user_id)
