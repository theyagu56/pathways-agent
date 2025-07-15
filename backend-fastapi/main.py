from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from routes.match_providers import router as match_providers_router
from routes.insurances import router as insurances_router

load_dotenv()

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