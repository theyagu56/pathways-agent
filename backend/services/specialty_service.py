from typing import List, Dict, Set
from services.provider_loader import get_providers
from utils.logger import get_logger

logger = get_logger(__name__)

class SpecialtyService:
    def __init__(self):
        self.providers = get_providers()
        self.available_specialties = self._extract_unique_specialties()
        logger.info(f"SpecialtyService initialized with {len(self.available_specialties)} unique specialties")
    
    def reload_data(self):
        """Reload provider data and re-extract specialties"""
        from services.provider_loader import clear_provider_cache
        clear_provider_cache()
        self.providers = get_providers()
        self.available_specialties = self._extract_unique_specialties()
        logger.info(f"SpecialtyService reloaded with {len(self.available_specialties)} unique specialties: {sorted(self.available_specialties)}")
    
    def _extract_unique_specialties(self) -> Set[str]:
        """Extract all unique specialties from providers data"""
        specialties = set()
        for provider in self.providers:
            if isinstance(provider, dict) and "specialty" in provider:
                specialties.add(provider["specialty"])
        logger.info(f"Extracted {len(specialties)} unique specialties: {sorted(specialties)}")
        return specialties
    
    def get_available_specialties(self) -> List[str]:
        """Get list of all available specialties"""
        return sorted(list(self.available_specialties))
    
    def get_specialty_recommendations(self, injury_description: str) -> List[str]:
        """Get specialty recommendations based on injury description using LLM"""
        logger.info(f"Getting LLM recommendations for injury: '{injury_description}'")
        return self._get_llm_recommendations(injury_description)
    
    def _get_llm_recommendations(self, injury_description: str) -> List[str]:
        """Use LLM to recommend specialties from available options"""
        try:
            from services.llm_client import LLMClient
            llm = LLMClient()
            
            # Pass available specialties to LLM for accurate recommendations
            available_specialties_list = sorted(list(self.available_specialties))
            logger.debug(f"Available specialties for LLM: {available_specialties_list}")
            
            specialties = llm.get_specialties(injury_description, available_specialties_list)
            
            # Filter to only include specialties that exist in our data
            filtered_specialties = [s for s in specialties if s in self.available_specialties]
            
            if filtered_specialties:
                logger.info(f"LLM recommended specialties (filtered): {filtered_specialties}")
                return filtered_specialties[:3]
            else:
                logger.warning("LLM recommendations not found in available specialties, using fallback")
                return self._get_fallback_specialties()
                
        except Exception as e:
            logger.error(f"Error getting LLM recommendations: {e}")
            return self._get_fallback_specialties()
    
    def _get_fallback_specialties(self) -> List[str]:
        """Get fallback specialties when LLM fails"""
        fallback_options = ["Orthopedics", "Sports Medicine", "Physical Therapy", "Primary Care", "Internal Medicine"]
        available_fallbacks = [s for s in fallback_options if s in self.available_specialties]
        logger.info(f"Using fallback specialties: {available_fallbacks[:3]}")
        return available_fallbacks[:3]
    
    def get_providers_by_specialty(self, specialty: str) -> List[Dict]:
        """Get all providers for a specific specialty"""
        providers = [p for p in self.providers if p.get("specialty") == specialty]
        logger.debug(f"Found {len(providers)} providers for specialty: {specialty}")
        return providers 