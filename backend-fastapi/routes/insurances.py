from fastapi import APIRouter
from services.provider_loader import get_providers

router = APIRouter()

@router.get("/api/insurances")
def get_insurances():
    providers = get_providers()
    insurances = set()
    for p in providers:
        insurances.update(p.get("insurances", []))
    return sorted(insurances) 