from datetime import datetime
from pydantic import BaseModel

class ReminderBase(BaseModel):
    title: str
    scheduled_for: datetime

class ReminderCreate(ReminderBase):
    user_id: int

class Reminder(ReminderBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
