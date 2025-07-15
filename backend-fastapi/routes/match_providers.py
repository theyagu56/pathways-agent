from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.llm_client import LLMClient
from services.vector_store import VectorStore
from services.provider_ranker import rank_providers
from services.provider_loader import get_providers

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
    try:
        providers = get_providers()
        llm = LLMClient()
        specialties = llm.get_specialties(request.injury_description)
        # Optionally use vector store for semantic search (not required for ranking demo)
        # vector_store = VectorStore()
        # doc_texts = [p["specialty"] + " " + p["name"] for p in providers]
        # top_indices = vector_store.embed_and_search(doc_texts, request.injury_description)
        # filtered_providers = [providers[i] for i in top_indices]
        ranked = rank_providers(providers, specialties, request.zip_code, request.insurance)
        # Convert to response model
        return [ProviderMatchResponse(**{
            "name": p["name"],
            "specialty": p["specialty"],
            "distance": p["distance"],
            "availability": p["availability"],
            "ranking_reason": p["ranking_reason"]
        }) for p in ranked]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider matching failed: {e}") 