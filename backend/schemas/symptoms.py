from pydantic import BaseModel

class Symptoms(BaseModel):
    symptoms: str
