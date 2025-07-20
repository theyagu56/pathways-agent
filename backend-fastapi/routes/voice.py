import os
import tempfile
import logging
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import JSONResponse
import sys
import os

# Add the parent directory to the path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.voice_service import VoiceService
from services.specialty_service import SpecialtyService
from services.llm_client import LLMClient
from utils.logger import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/voice", tags=["voice"])

# Initialize services
voice_service = VoiceService()
specialty_service = SpecialtyService()
llm_client = LLMClient()

@router.post("/upload-audio")
async def upload_and_process_audio(
    audio_file: UploadFile = File(...),
    insurance: str = Form("")  # Make insurance optional, will be extracted from audio
) -> Dict[str, Any]:
    """
    Upload audio file and process it to extract:
    - Symptoms/injury description
    - Zip code/location
    - Recommended specialties
    """
    try:
        logger.info(f"Processing audio upload: {audio_file.filename}")
        
        # Validate file type
        if not audio_file.content_type or not audio_file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Process audio with voice service
            voice_result = voice_service.process_audio_file(temp_file_path)
            
            logger.info(f"Voice processing completed: {voice_result['transcription'][:100]}...")
            
            # Get specialty recommendations using LLM
            injury_description = voice_result["symptoms"]
            zip_code = voice_result["location"]
            extracted_insurance = voice_result.get("structured_data", {}).get("insurance", "")
            
            if not zip_code:
                logger.warning("No zip code found in audio, using empty string")
                zip_code = ""
            
            # Get specialty recommendations
            specialty_recommendations = specialty_service.get_specialty_recommendations(injury_description)
            
            # Get provider matches
            from services.provider_ranker import rank_providers
            from services.provider_loader import get_providers
            
            providers = get_providers()
            
            # Filter providers by specialty recommendations
            matching_providers = []
            for provider in providers:
                if provider.get("specialty") in specialty_recommendations:
                    matching_providers.append(provider)
            
            # Rank providers
            ranked_providers = rank_providers(
                matching_providers, 
                specialty_recommendations,
                zip_code,
                extracted_insurance
            )
            
            return {
                "success": True,
                "voice_processing": {
                    "transcription": voice_result["transcription"],
                    "confidence": voice_result["confidence"],
                    "processing_method": voice_result["processing_method"]
                },
                "extracted_info": {
                    "symptoms": voice_result["symptoms"],
                    "zip_code": voice_result["location"],
                    "insurance": extracted_insurance
                },
                "specialty_recommendations": specialty_recommendations,
                "providers": ranked_providers[:3],  # Top 3 providers
                "total_providers_found": len(ranked_providers)
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        logger.error(f"Error processing audio upload: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}")

@router.post("/process-text")
async def process_text_input(
    text_input: str = Form(...),
    insurance: str = Form("")  # Make insurance optional, will be extracted from text
) -> Dict[str, Any]:
    """
    Process text input (alternative to voice) and get provider matches
    """
    try:
        logger.info(f"Processing text input: {text_input[:100]}...")
        
        # Use voice service to extract structured information from text
        voice_result = voice_service._extract_structured_info(text_input)
        
        # Extract information from voice service result
        injury_description = voice_result["symptoms"]
        zip_code = voice_result["location"]
        insurance = voice_result.get("structured_data", {}).get("insurance", "")
        
        # Get specialty recommendations using the extracted injury description
        specialty_recommendations = specialty_service.get_specialty_recommendations(injury_description)
        
        # Get provider matches
        from services.provider_ranker import rank_providers
        from services.provider_loader import get_providers
        
        providers = get_providers()
        
        # Filter providers by specialty recommendations
        matching_providers = []
        for provider in providers:
            if provider.get("specialty") in specialty_recommendations:
                matching_providers.append(provider)
        
        # Rank providers
        ranked_providers = rank_providers(
            matching_providers, 
            specialty_recommendations,
            zip_code,
            insurance
        )
        
        return {
            "success": True,
            "extracted_info": {
                "symptoms": injury_description,
                "zip_code": zip_code,
                "insurance": insurance
            },
            "specialty_recommendations": specialty_recommendations,
            "providers": ranked_providers[:3],  # Top 3 providers
            "total_providers_found": len(ranked_providers),
            "structured_data": voice_result.get("structured_data", {})
        }
        
    except Exception as e:
        logger.error(f"Error processing text input: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing text: {str(e)}")

@router.get("/health")
async def get_voice_service_health() -> Dict[str, Any]:
    """Get health status of voice processing services"""
    try:
        health_status = voice_service.get_health_status()
        return {
            "success": True,
            "voice_services": health_status,
            "message": "Voice services are operational"
        }
    except Exception as e:
        logger.error(f"Error getting voice service health: {e}")
        return {
            "success": False,
            "voice_services": {},
            "error": str(e)
        }

@router.post("/test-audio")
async def test_audio_processing(
    audio_file: UploadFile = File(...)
) -> Dict[str, Any]:
    """
    Test endpoint to just transcribe audio without full processing
    """
    try:
        logger.info(f"Testing audio processing: {audio_file.filename}")
        
        # Validate file type
        if not audio_file.content_type or not audio_file.content_type.startswith("audio/"):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        try:
            # Process audio with voice service
            voice_result = voice_service.process_audio_file(temp_file_path)
            
            return {
                "success": True,
                "transcription": voice_result["transcription"],
                "confidence": voice_result["confidence"],
                "processing_method": voice_result["processing_method"],
                "extracted_info": {
                    "symptoms": voice_result["symptoms"],
                    "location": voice_result["location"]
                }
            }
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        logger.error(f"Error testing audio processing: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing audio: {str(e)}") 