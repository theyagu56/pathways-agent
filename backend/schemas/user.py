from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    full_name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
