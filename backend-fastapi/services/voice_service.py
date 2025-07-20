import os
import tempfile
import logging
from typing import Dict, Any, Optional, Tuple
import whisper
from pydub import AudioSegment
import numpy as np
import soundfile as sf
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
from azure.cognitiveservices.speech.audio import AudioInputStream
import azure.cognitiveservices.speech as speechsdk

logger = logging.getLogger(__name__)

class VoiceService:
    def __init__(self):
        self.whisper_model = None
        self.azure_speech_config = None
        self.use_azure = os.getenv("USE_AZURE_SPEECH", "false").lower() == "true"
        
        # Initialize Whisper model (lazy loading)
        self._init_whisper()
        
        # Initialize Azure Speech Services if configured
        if self.use_azure:
            self._init_azure_speech()
    
    def _init_whisper(self):
        """Initialize Whisper model for local transcription"""
        try:
            logger.info("Loading Whisper model...")
            self.whisper_model = whisper.load_model("base")
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            self.whisper_model = None
    
    def _init_azure_speech(self):
        """Initialize Azure Speech Services configuration"""
        try:
            azure_key = os.getenv("AZURE_SPEECH_KEY")
            azure_region = os.getenv("AZURE_SPEECH_REGION")
            
            if not azure_key or not azure_region:
                logger.warning("Azure Speech Services not configured, falling back to Whisper")
                self.use_azure = False
                return
            
            self.azure_speech_config = SpeechConfig(
                subscription=azure_key, 
                region=azure_region
            )
            self.azure_speech_config.speech_recognition_language = "en-US"
            logger.info("Azure Speech Services configured successfully")
            
        except Exception as e:
            logger.error(f"Failed to configure Azure Speech Services: {e}")
            self.use_azure = False
    
    def process_audio_file(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Process audio file and extract transcription, symptoms, location, and specialty recommendations
        
        Returns:
            Dict containing:
            - transcription: Raw transcribed text
            - symptoms: Extracted symptoms/injury description
            - location: Extracted zip code or location
            - confidence: Transcription confidence score
            - processing_method: "azure" or "whisper"
        """
        try:
            logger.info(f"Processing audio file: {audio_file_path}")
            
            # Convert audio to proper format if needed
            processed_audio_path = self._preprocess_audio(audio_file_path)
            
            # Transcribe audio
            if self.use_azure and self.azure_speech_config:
                transcription_result = self._transcribe_with_azure(processed_audio_path)
            else:
                transcription_result = self._transcribe_with_whisper(processed_audio_path)
            
            # Extract structured information from transcription
            extracted_info = self._extract_structured_info(transcription_result["transcription"])
            
            # Clean up temporary files
            if processed_audio_path != audio_file_path:
                os.remove(processed_audio_path)
            
            return {
                **extracted_info,
                "confidence": transcription_result["confidence"],
                "processing_method": transcription_result["method"]
            }
            
        except Exception as e:
            logger.error(f"Error processing audio file: {e}")
            raise
    
    def _preprocess_audio(self, audio_path: str) -> str:
        """Preprocess audio file to ensure compatibility"""
        try:
            # Check if ffmpeg is available
            import subprocess
            try:
                subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
                ffmpeg_available = True
                logger.info("ffmpeg is available for audio processing")
            except (subprocess.CalledProcessError, FileNotFoundError):
                ffmpeg_available = False
                logger.warning("ffmpeg not available, audio preprocessing may fail")
            
            # Load audio with pydub
            audio = AudioSegment.from_file(audio_path)
            
            # Convert to mono if stereo
            if audio.channels > 1:
                audio = audio.set_channels(1)
            
            # Ensure sample rate is 16kHz (optimal for Whisper)
            if audio.frame_rate != 16000:
                audio = audio.set_frame_rate(16000)
            
            # Export to temporary WAV file
            temp_path = tempfile.mktemp(suffix=".wav")
            audio.export(temp_path, format="wav")
            
            logger.info(f"Audio preprocessed: {audio_path} -> {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.warning(f"Audio preprocessing failed, using original: {e}")
            return audio_path
    
    def _transcribe_with_whisper(self, audio_path: str) -> Dict[str, Any]:
        """Transcribe audio using OpenAI Whisper"""
        try:
            if not self.whisper_model:
                raise Exception("Whisper model not loaded")
            
            logger.info("Transcribing with Whisper...")
            result = self.whisper_model.transcribe(audio_path)
            
            return {
                "transcription": result["text"].strip(),
                "confidence": result.get("confidence", 0.0),
                "method": "whisper"
            }
            
        except Exception as e:
            logger.error(f"Whisper transcription failed: {e}")
            raise
    
    def _transcribe_with_azure(self, audio_path: str) -> Dict[str, Any]:
        """Transcribe audio using Azure Speech Services"""
        try:
            logger.info("Transcribing with Azure Speech Services...")
            
            # Create audio config
            audio_config = AudioConfig(filename=audio_path)
            
            # Create recognizer
            recognizer = SpeechRecognizer(
                speech_config=self.azure_speech_config, 
                audio_config=audio_config
            )
            
            # Perform recognition
            result = recognizer.recognize_once()
            
            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                return {
                    "transcription": result.text.strip(),
                    "confidence": 0.9,  # Azure doesn't provide confidence in this API
                    "method": "azure"
                }
            else:
                raise Exception(f"Azure recognition failed: {result.reason}")
                
        except Exception as e:
            logger.error(f"Azure transcription failed: {e}")
            # Fallback to Whisper
            logger.info("Falling back to Whisper...")
            return self._transcribe_with_whisper(audio_path)
    
    def _extract_structured_info(self, transcription: str) -> Dict[str, Any]:
        """
        Extract structured information from transcription using LLM:
        - Medically relevant symptoms/injury description only
        - Zip code or location
        - Structured JSON output
        """
        try:
            logger.info(f"Extracting structured info from: {transcription}")
            
            # Use LLM to extract structured medical information
            structured_info = self._extract_medical_info_with_llm(transcription)
            
            return {
                "transcription": transcription,
                "symptoms": structured_info.get("injury_description", transcription),
                "location": structured_info.get("zip_code", ""),
                "raw_text": transcription,
                "structured_data": structured_info
            }
            
        except Exception as e:
            logger.error(f"Error extracting structured info: {e}")
            # Fallback to basic extraction
            import re
            zip_pattern = r'\b\d{5}\b'
            zip_matches = re.findall(zip_pattern, transcription)
            location = zip_matches[0] if zip_matches else ""
            
            return {
                "transcription": transcription,
                "symptoms": transcription,
                "location": location,
                "raw_text": transcription,
                "structured_data": {
                    "injury_description": transcription,
                    "zip_code": location
                }
            }
    
    def _extract_medical_info_with_llm(self, transcription: str) -> Dict[str, Any]:
        """
        Use LLM to extract only medically relevant information from transcription
        """
        try:
            from services.llm_client import LLMClient
            llm_client = LLMClient()
            
            prompt = f"""
You are a medical information extraction specialist. Extract ONLY medically relevant symptoms, injuries, or conditions from the patient's description.

IMPORTANT RULES:
1. Focus ONLY on medical symptoms, injuries, or conditions - ignore context, stories, or non-medical details
2. Extract zip code if present (5-digit format)
3. Extract insurance provider if mentioned (e.g., "Blue Cross", "Aetna", "Cigna", "UnitedHealth", "Medicare", "Humana", "Kaiser")
4. Return ONLY valid JSON - no additional text, explanations, or formatting
5. Use clear, concise medical terminology
6. If no medical symptoms found, use "No specific symptoms mentioned"

Available specialties: Allergy, Anesthesiology, Cardiology, Dentist, Dermatology, ENT, Endocrinology, Gastroenterology, General Surgery, Hematology, Immunology, Infectious Disease, Nephrology, Neurology, Oncology, Ophthalmology, Orthopedics, Pathology, Pediatrics, Physical Therapy, Plastic Surgery, Psychiatry, Pulmonology, Radiology, Rheumatology, Sports Medicine, Urology

Patient description: "{transcription}"

Return JSON in this exact format:
{{
  "injury_description": "extracted medical symptoms/injuries only",
  "zip_code": "extracted zip code or empty string",
  "insurance": "extracted insurance provider or empty string",
  "recommended_specialties": ["specialty1", "specialty2"]
}}

JSON:
"""
            
            logger.info("Using LLM to extract medical information")
            response = llm_client.client.invoke(prompt)
            response_text = response.content.strip()
            
            # Parse JSON response
            import json
            import re
            
            # Find JSON in response (handle cases where LLM adds extra text)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                structured_data = json.loads(json_str)
                
                # Validate required fields
                if "injury_description" not in structured_data:
                    structured_data["injury_description"] = "No specific symptoms mentioned"
                if "zip_code" not in structured_data:
                    structured_data["zip_code"] = ""
                if "insurance" not in structured_data:
                    structured_data["insurance"] = ""
                if "recommended_specialties" not in structured_data:
                    structured_data["recommended_specialties"] = []
                
                logger.info(f"Extracted structured data: {structured_data}")
                return structured_data
            else:
                logger.warning("No JSON found in LLM response, using fallback")
                return self._fallback_extraction(transcription)
                
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            return self._fallback_extraction(transcription)
    
    def _fallback_extraction(self, transcription: str) -> Dict[str, Any]:
        """
        Fallback method for extracting information when LLM fails
        """
        import re
        
        # Extract zip code
        zip_pattern = r'\b\d{5}\b'
        zip_matches = re.findall(zip_pattern, transcription)
        zip_code = zip_matches[0] if zip_matches else ""
        
        # Simple keyword-based specialty detection
        specialties = []
        text_lower = transcription.lower()
        
        specialty_keywords = {
            "Dentist": ["tooth", "teeth", "dental", "mouth", "gum"],
            "Cardiology": ["chest pain", "heart", "cardiac", "palpitation"],
            "Neurology": ["headache", "head injury", "brain", "seizure"],
            "Orthopedics": ["broken", "fracture", "bone", "joint", "knee", "shoulder"],
            "Dermatology": ["rash", "skin", "itch", "burn"],
            "ENT": ["ear", "nose", "throat", "hearing", "swallowing"],
            "Ophthalmology": ["eye", "vision", "blind", "sight"],
            "Psychiatry": ["anxiety", "depression", "mental", "mood"]
        }
        
        for specialty, keywords in specialty_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                specialties.append(specialty)
        
        # If no specialties found, add general ones
        if not specialties:
            specialties = ["General Surgery", "Primary Care"]
        
        # Extract insurance keywords
        insurance_keywords = {
            "Blue Cross": ["blue cross", "bluecross"],
            "Aetna": ["aetna"],
            "Cigna": ["cigna"],
            "UnitedHealth": ["unitedhealth", "united health"],
            "Medicare": ["medicare"],
            "Humana": ["humana"],
            "Kaiser": ["kaiser", "kaiser permanente"]
        }
        
        insurance = ""
        text_lower = transcription.lower()
        for ins_name, keywords in insurance_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                insurance = ins_name
                break
        
        return {
            "injury_description": transcription,
            "zip_code": zip_code,
            "insurance": insurance,
            "recommended_specialties": specialties[:3]  # Limit to 3
        }
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get the health status of voice processing services"""
        return {
            "whisper_available": self.whisper_model is not None,
            "azure_available": self.use_azure and self.azure_speech_config is not None,
            "preferred_method": "azure" if self.use_azure else "whisper"
        } 