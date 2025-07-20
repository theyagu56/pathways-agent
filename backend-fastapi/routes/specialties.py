from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.specialty_service import SpecialtyService
from services.provider_loader import clear_provider_cache
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

class SpecialtyRecommendationRequest(BaseModel):
    injury_description: str

@router.get("/api/specialties")
def get_specialties():
    """Get all available specialties from providers data"""
    try:
        logger.info("Fetching available specialties from providers")
        specialty_service = SpecialtyService()
        specialties = specialty_service.get_available_specialties()
        logger.info(f"Returning {len(specialties)} available specialties")
        return specialties
    except Exception as e:
        logger.error(f"Error in get_specialties: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch specialties: {str(e)}")

@router.post("/api/specialty-recommendations")
def get_specialty_recommendations(request: SpecialtyRecommendationRequest):
    """Get specialty recommendations based on injury description"""
    try:
        logger.info(f"Getting specialty recommendations for injury: '{request.injury_description}'")
        specialty_service = SpecialtyService()
        recommendations = specialty_service.get_specialty_recommendations(request.injury_description)
        logger.info(f"Returning {len(recommendations)} specialty recommendations: {recommendations}")
        return {
            "injury_description": request.injury_description,
            "recommended_specialties": recommendations,
            "available_specialties": specialty_service.get_available_specialties()
        }
    except Exception as e:
        logger.error(f"Error in get_specialty_recommendations: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get specialty recommendations: {str(e)}")

@router.post("/api/clear-cache")
def clear_cache():
    """Clear provider cache and reload data"""
    try:
        logger.info("Clearing provider cache and reloading SpecialtyService")
        clear_provider_cache()
        
        # Create a new SpecialtyService instance to reload data
        specialty_service = SpecialtyService()
        specialty_service.reload_data()
        
        logger.info("Provider cache and SpecialtyService cleared successfully")
        return {"message": "Cache cleared successfully", "specialties_count": len(specialty_service.get_available_specialties())}
    except Exception as e:
        logger.error(f"Error clearing cache: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to clear cache: {str(e)}") 