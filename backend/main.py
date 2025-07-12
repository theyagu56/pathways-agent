from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os


load_dotenv()

# Determine allowed origins for CORS
allowed_origins_setting = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins_setting == "*":
    origins = ["*"]
else:
    origins = [origin.strip() for origin in allowed_origins_setting.split(",") if origin.strip()]

from database import engine, Base
from routers import user_router, reminder_router, symptoms_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Patient Copilot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(reminder_router)
app.include_router(symptoms_router)


@app.get("/")
def read_root():
    return {"message": "Patient Copilot API"}
