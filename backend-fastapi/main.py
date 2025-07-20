# Initialize logging first
from utils.logger import get_logger
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get logger for main module
logger = get_logger(__name__)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.match_providers import router as match_providers_router
from routes.insurances import router as insurances_router
from routes.specialties import router as specialties_router
from routes.voice import router as voice_router

logger.info("Starting Pathways AI Provider Matching API")

app = FastAPI(title="Pathways Agent Provider Matching API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(match_providers_router)
app.include_router(insurances_router)
app.include_router(specialties_router)
app.include_router(voice_router)

logger.info("FastAPI app configured with CORS and routers")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Pathways AI Provider Matching API is running"}

logger.info("Application startup complete")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Pathways Agent Provider Matching API...")
    print("📋 Configuration:")
    print(f"   - OpenAI API Key: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Missing'}")
    print(f"   - Azure Speech Services: {'✅ Configured' if os.getenv('AZURE_SPEECH_KEY') else '❌ Not configured'}")
    print(f"   - Providers file: Will auto-detect from multiple possible locations")
    print("🌐 Server will be available at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("🎤 Voice Processing: Available at /api/voice/*")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 