from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
from typing import List, Optional
import openai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Pathways Agent Provider Matching API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProviderMatchRequest(BaseModel):
    injury_description: str
    zip_code: str
    insurance: str

class Provider(BaseModel):
    id: str
    name: str
    specialty: str
    zip_code: str
    insurances: List[str]
    rating: float
    distance: float
    availability_date: str

class ProviderMatchResponse(BaseModel):
    name: str
    specialty: str
    distance: float
    availability: str
    ranking_reason: str

def load_providers() -> List[dict]:
    """Load providers from the shared JSON file"""
    try:
        # Use absolute path
        providers_path = "/Users/thiyagarajankamalakannan/Projects/CursorPathwayAgent/pathways-ai/shared-data/providers.json"
        
        with open(providers_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Provider data not found at {providers_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading providers: {str(e)}")

def get_specialty_recommendations(injury_description: str) -> List[str]:
    """Use GPT-4 to recommend specialties based on injury description"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a medical specialist who recommends the most appropriate medical specialties for treating specific injuries or conditions. Return only 2-3 specialty names, separated by commas."
                },
                {
                    "role": "user",
                    "content": f"Based on this injury description: '{injury_description}', what are the 2-3 most appropriate medical specialties for treatment? Return only the specialty names separated by commas."
                }
            ],
            max_tokens=100,
            temperature=0.3
        )
        
        # Add null check for the response
        content = response.choices[0].message.content
        if content is None:
            return ["Orthopedics", "Sports Medicine", "Physical Therapy"]
            
        specialties = content.strip().split(",")
        return [s.strip() for s in specialties]
    except Exception as e:
        # Fallback to common specialties if OpenAI fails
        return ["Orthopedics", "Sports Medicine", "Physical Therapy"]

def calculate_distance(zip1: str, zip2: str) -> float:
    """Calculate approximate distance between zip codes (mock implementation)"""
    # Simple mock distance calculation
    zip1_num = int(zip1[:5]) if zip1.isdigit() else 10000
    zip2_num = int(zip2[:5]) if zip2.isdigit() else 10000
    return abs(zip1_num - zip2_num) / 1000.0

def rank_providers(providers: List[dict], recommended_specialties: List[str], 
                   target_zip: str, target_insurance: str) -> List[ProviderMatchResponse]:
    """Rank providers based on specialty match, distance, and insurance"""
    ranked_providers = []
    
    for provider in providers:
        # Calculate specialty match score
        specialty_match = 1.0 if provider["specialty"] in recommended_specialties else 0.3
        
        # Calculate distance
        distance = calculate_distance(target_zip, provider["zip_code"])
        
        # Check insurance compatibility
        insurance_match = 1.0 if target_insurance in provider["insurances"] else 0.5
        
        # Calculate overall score (weighted combination)
        score = (specialty_match * 0.5) + (insurance_match * 0.3) + (1.0 / (1.0 + distance) * 0.2)
        
        # Create ranking reason
        reasons = []
        if specialty_match > 0.8:
            reasons.append("Specialty match")
        if insurance_match > 0.8:
            reasons.append("Insurance accepted")
        if distance < 10:
            reasons.append("Close proximity")
        
        ranking_reason = ", ".join(reasons) if reasons else "General match"
        
        ranked_providers.append({
            "provider": provider,
            "score": score,
            "ranking_reason": ranking_reason
        })
    
    # Sort by score and return top results
    ranked_providers.sort(key=lambda x: x["score"], reverse=True)
    
    return [
        ProviderMatchResponse(
            name=p["provider"]["name"],
            specialty=p["provider"]["specialty"],
            distance=p["provider"]["distance"],
            availability=p["provider"]["availability_date"],
            ranking_reason=p["ranking_reason"]
        )
        for p in ranked_providers[:5]  # Return top 5 matches
    ]

@app.post("/api/match-providers", response_model=List[ProviderMatchResponse])
async def match_providers(request: ProviderMatchRequest):
    """Match providers based on injury description, location, and insurance"""
    try:
        # Load providers
        providers = load_providers()
        
        # Get specialty recommendations from GPT-4
        recommended_specialties = get_specialty_recommendations(request.injury_description)
        
        # Rank and filter providers
        ranked_providers = rank_providers(
            providers, 
            recommended_specialties, 
            request.zip_code, 
            request.insurance
        )
        
        return ranked_providers
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching providers: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Pathways Agent Provider Matching API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 