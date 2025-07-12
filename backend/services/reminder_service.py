from sqlalchemy.orm import Session


from models.reminder import Reminder
from schemas import reminder as schemas



def create_reminder(db: Session, reminder: schemas.ReminderCreate):
    db_reminder = Reminder(
        title=reminder.title,
        scheduled_for=reminder.scheduled_for,
        user_id=reminder.user_id
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder


def get_reminders(db: Session, user_id: int):
    return db.query(Reminder).filter(Reminder.user_id == user_id).all()
