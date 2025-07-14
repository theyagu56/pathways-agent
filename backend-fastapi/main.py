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
        # Try multiple possible paths for different environments
        possible_paths = [
            # Relative path from backend directory
            "../shared-data/providers.json",
            # Absolute path for local development
            "/Users/thiyagarajankamalakannan/Projects/CursorPathwayAgent/pathways-ai/shared-data/providers.json",
            # Codespace/container path
            "./shared-data/providers.json",
            # Alternative relative path
            "../../shared-data/providers.json"
        ]
        
        providers_path = None
        for path in possible_paths:
            if os.path.exists(path):
                providers_path = path
                break
        
        if not providers_path:
            error_msg = f"❌ Provider data file not found. Tried paths: {possible_paths}"
            print(error_msg)
            print("💡 Make sure the shared-data/providers.json file exists")
            raise HTTPException(status_code=500, detail=error_msg)
        
        print(f"📁 Loading providers from: {providers_path}")
        
        with open(providers_path, "r") as f:
            providers = json.load(f)
            print(f"✅ Successfully loaded {len(providers)} providers")
            return providers
            
    except FileNotFoundError:
        error_msg = f"❌ Provider data file not found at: {providers_path}"
        print(error_msg)
        print("💡 Make sure the shared-data/providers.json file exists")
        raise HTTPException(status_code=500, detail=error_msg)
    except json.JSONDecodeError as e:
        error_msg = f"❌ Invalid JSON format in providers file: {str(e)}"
        print(error_msg)
        print("💡 Check that the providers.json file contains valid JSON")
        raise HTTPException(status_code=500, detail=error_msg)
    except Exception as e:
        error_msg = f"❌ Unexpected error loading providers: {str(e)}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

def get_specialty_recommendations(injury_description: str) -> List[str]:
    """Use GPT-4 to recommend specialties based on injury description"""
    try:
        from openai import OpenAI
        
        # Check if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("⚠️  Warning: OPENAI_API_KEY not found in environment variables. Using fallback specialties.")
            return ["Orthopedics", "Sports Medicine", "Physical Therapy"]
        
        client = OpenAI(api_key=api_key)
        
        print(f"🤖 Calling OpenAI GPT-4 for injury: '{injury_description}'")
        
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
            print("⚠️  Warning: OpenAI returned empty response. Using fallback specialties.")
            return ["Orthopedics", "Sports Medicine", "Physical Therapy"]
            
        specialties = content.strip().split(",")
        result = [s.strip() for s in specialties]
        print(f"✅ OpenAI recommended specialties: {result}")
        return result
        
    except ImportError as e:
        print(f"❌ Error: OpenAI library not installed. Please run: pip install openai")
        return ["Orthopedics", "Sports Medicine", "Physical Therapy"]
    except Exception as e:
        print(f"❌ OpenAI API Error: {str(e)}")
        print("🔄 Using fallback specialties due to API error")
        return ["Orthopedics", "Sports Medicine", "Physical Therapy"]

def calculate_distance(zip1: str, zip2: str) -> float:
    """Calculate approximate distance between zip codes (mock implementation)"""
    try:
        # Validate zip codes
        if not zip1 or not zip2:
            print(f"⚠️  Warning: Invalid zip codes provided: '{zip1}' and '{zip2}'")
            return 50.0  # Default distance for invalid zips
        
        # Simple mock distance calculation
        zip1_num = int(zip1[:5]) if zip1.isdigit() else 10000
        zip2_num = int(zip2[:5]) if zip2.isdigit() else 10000
        distance = abs(zip1_num - zip2_num) / 1000.0
        
        return distance
        
    except ValueError as e:
        print(f"⚠️  Warning: Could not convert zip codes to numbers: '{zip1}', '{zip2}'. Error: {str(e)}")
        return 50.0  # Default distance
    except Exception as e:
        print(f"⚠️  Warning: Error calculating distance between '{zip1}' and '{zip2}': {str(e)}")
        return 50.0  # Default distance

def rank_providers(providers: List[dict], recommended_specialties: List[str], 
                   target_zip: str, target_insurance: str) -> List[ProviderMatchResponse]:
    """Rank providers based on specialty match, distance, and insurance"""
    try:
        print(f"📊 Ranking {len(providers)} providers...")
        print(f"🎯 Target specialties: {recommended_specialties}")
        
        ranked_providers = []
        
        for i, provider in enumerate(providers):
            try:
                # Validate provider data structure
                required_fields = ["name", "specialty", "zip_code", "insurances", "distance", "availability_date"]
                for field in required_fields:
                    if field not in provider:
                        print(f"⚠️  Warning: Provider {i} missing field '{field}', skipping")
                        continue
                
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
                
            except Exception as e:
                print(f"⚠️  Warning: Error processing provider {i} ({provider.get('name', 'Unknown')}): {str(e)}")
                continue
        
        # Sort by score and return top results
        ranked_providers.sort(key=lambda x: x["score"], reverse=True)
        
        result = [
            ProviderMatchResponse(
                name=p["provider"]["name"],
                specialty=p["provider"]["specialty"],
                distance=p["provider"]["distance"],
                availability=p["provider"]["availability_date"],
                ranking_reason=p["ranking_reason"]
            )
            for p in ranked_providers[:5]  # Return top 5 matches
        ]
        
        print(f"✅ Successfully ranked providers. Top score: {ranked_providers[0]['score'] if ranked_providers else 'N/A'}")
        return result
        
    except Exception as e:
        print(f"❌ Error in provider ranking: {str(e)}")
        raise Exception(f"Failed to rank providers: {str(e)}")

@app.post("/api/match-providers", response_model=List[ProviderMatchResponse])
async def match_providers(request: ProviderMatchRequest):
    """Match providers based on injury description, location, and insurance"""
    try:
        print(f"🔍 Starting provider matching for:")
        print(f"   Injury: {request.injury_description}")
        print(f"   ZIP: {request.zip_code}")
        print(f"   Insurance: {request.insurance}")
        
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
        
        print(f"✅ Found {len(ranked_providers)} matching providers")
        return ranked_providers
        
    except HTTPException:
        # Re-raise HTTP exceptions as they already have proper error details
        raise
    except Exception as e:
        error_msg = f"❌ Unexpected error in provider matching: {str(e)}"
        print(error_msg)
        print(f"💡 Error type: {type(e).__name__}")
        import traceback
        print(f"📋 Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/")
async def root():
    return {"message": "Pathways Agent Provider Matching API"}

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Pathways Agent Provider Matching API...")
    print("📋 Configuration:")
    print(f"   - OpenAI API Key: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    print(f"   - Providers file: Will auto-detect from multiple possible locations")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 