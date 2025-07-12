from fastapi import APIRouter
from schemas import Symptoms

router = APIRouter(tags=["symptoms"])

@router.post("/symptoms")
def submit_symptoms(symptoms: Symptoms):
    message = (
        f"OK, we got your symptoms: {symptoms.symptoms}. "
        "We are going to do some further analysis and get back to you."
    )
    return {"message": message}
