import os
from typing import List
from utils.logger import get_logger

logger = get_logger(__name__)

class LLMClient:
    def __init__(self):
        self.use_azure = os.getenv("USE_AZURE_OPENAI", "false").lower() == "true"
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the LLM client based on environment configuration"""
        try:
            if self.use_azure:
                logger.info("LLM Configuration - Use Azure: True")
                from langchain_openai import AzureChatOpenAI
                
                self.client = AzureChatOpenAI(
                    azure_deployment=os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4"),
                    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
                    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                    temperature=0.1
                )
                logger.info("Azure OpenAI client initialized successfully")
            else:
                logger.info("LLM Configuration - Use Azure: False")
                from langchain_openai import ChatOpenAI
                
                self.client = ChatOpenAI(
                    model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                    openai_api_key=os.getenv("OPENAI_API_KEY"),
                    temperature=0.1
                )
                logger.info("OpenAI client initialized successfully")
                
        except Exception as e:
            logger.error(f"Failed to initialize LLM client: {e}")
            raise
    
    def get_specialties(self, injury_description: str, available_specialties: List[str] = None) -> List[str]:
        """Get specialty recommendations from LLM"""
        try:
            logger.info("Making LLM API call for specialty recommendation")
            
            if available_specialties:
                specialties_list = ", ".join(sorted(available_specialties))
                prompt = f"""You are a medical specialist who recommends the most appropriate medical specialties for treating specific injuries or conditions.

Available specialties in our system: {specialties_list}

Based on this injury description: '{injury_description}', what are the 2-3 most appropriate medical specialties from the available list above? Return only the specialty names separated by commas.

Specialties:"""
            else:
                prompt = f"""You are a medical specialist who recommends the most appropriate medical specialties for treating specific injuries or conditions.

Based on this injury description: '{injury_description}', what are the 2-3 most appropriate medical specialties? Return only the specialty names separated by commas.

Specialties:"""
            
            logger.info(prompt)
            response = self.client.invoke(prompt)
            raw_response = response.content.strip()
            
            logger.info(f"LLM response received - Raw: '{raw_response}'")
            
            # Parse the response to extract specialty names
            specialties = [s.strip() for s in raw_response.split(',')]
            logger.info(f"Parsed specialties: {specialties}")
            
            return specialties
            
        except Exception as e:
            logger.error(f"Error in LLM call: {e}")
            return [] 