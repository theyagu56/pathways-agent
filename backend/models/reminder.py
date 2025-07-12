from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    scheduled_for = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User")
