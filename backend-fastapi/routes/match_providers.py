from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.llm_client import LLMClient
from services.vector_store import VectorStore
from services.provider_ranker import rank_providers
from services.provider_loader import get_providers
from utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()

class ProviderMatchRequest(BaseModel):
    injury_description: str
    zip_code: str
    insurance: str

class ProviderMatchResponse(BaseModel):
    name: str
    specialty: str
    distance: float
    availability: str
    ranking_reason: str

@router.post("/api/match-providers", response_model=List[ProviderMatchResponse])
async def match_providers(request: ProviderMatchRequest):
    logger.info(f"Provider matching request received - Injury: '{request.injury_description}', ZIP: {request.zip_code}, Insurance: {request.insurance}")
    
    try:
        logger.debug("Loading providers from JSON file")
        providers = get_providers()
        logger.info(f"Loaded {len(providers)} providers from data source")
        
        logger.debug("Initializing LLM client for specialty recommendation")
        llm = LLMClient()
        
        logger.debug("Getting specialty recommendations from LLM")
        specialties = llm.get_specialties(request.injury_description)
        logger.info(f"LLM recommended specialties: {specialties}")
        
        # Optionally use vector store for semantic search (not required for ranking demo)
        # logger.debug("Initializing vector store for semantic search")
        # vector_store = VectorStore()
        # doc_texts = [p["specialty"] + " " + p["name"] for p in providers]
        # top_indices = vector_store.embed_and_search(doc_texts, request.injury_description)
        # filtered_providers = [providers[i] for i in top_indices]
        
        logger.debug("Ranking providers based on specialties, location, and insurance")
        ranked = rank_providers(providers, specialties, request.zip_code, request.insurance)
        
        # Convert to response model
        response_data = []
        for p in ranked:
            response_data.append(ProviderMatchResponse(**{
                "name": p["name"],
                "specialty": p["specialty"],
                "distance": p["distance"],
                "availability": p["availability"],
                "ranking_reason": p["ranking_reason"]
            }))
        
        logger.info(f"Provider matching completed successfully - Returning {len(response_data)} providers")
        return response_data
        
    except Exception as e:
        logger.error(f"Provider matching failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Provider matching failed: {e}") 