from fastapi import APIRouter, HTTPException
from services.provider_loader import get_providers
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

@router.get("/api/insurances")
def get_insurances():
    try:
        logger.info("Fetching insurance options from providers")
        providers = get_providers()
        logger.info(f"Loaded {len(providers)} providers")
        
        insurances = set()
        for i, p in enumerate(providers):
            try:
                if isinstance(p, dict) and "insurances" in p:
                    insurances.update(p.get("insurances", []))
                else:
                    logger.warning(f"Provider {i} has invalid structure: {type(p)}")
            except Exception as e:
                logger.error(f"Error processing provider {i}: {e}")
                continue
        
        result = sorted(insurances)
        logger.info(f"Returning {len(result)} unique insurance options: {result}")
        return result
        
    except Exception as e:
        logger.error(f"Error in get_insurances: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to fetch insurance options: {str(e)}") 