from sqlalchemy.orm import Session
from fastapi import HTTPException


from models.user import User
from schemas import user as schemas



def create_user(db: Session, user: schemas.UserCreate):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(email=user.email, full_name=user.full_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
