import os
from langchain_community.chat_models import ChatOpenAI, AzureChatOpenAI
from utils.logger import get_logger

logger = get_logger(__name__)

class LLMClient:
    def __init__(self):
        logger.debug("Initializing LLMClient")
        use_azure = os.getenv("USE_AZURE_OPENAI", "false").lower() == "true"
        self.use_azure = use_azure
        self.client = None
        
        logger.info(f"LLM Configuration - Use Azure: {use_azure}")
        
        try:
            if use_azure:
                logger.debug("Configuring Azure OpenAI client")
                azure_key = os.getenv("AZURE_OPENAI_API_KEY")
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
                deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
                
                logger.debug(f"Azure config - Key present: {bool(azure_key)}, Endpoint: {azure_endpoint}, Deployment: {deployment_name}")
                
                if not (azure_key and azure_endpoint and deployment_name):
                    logger.error("Azure OpenAI configuration missing in .env. Falling back to default specialties.")
                    logger.debug("Missing configs - Key: %s, Endpoint: %s, Deployment: %s", 
                               bool(azure_key), bool(azure_endpoint), bool(deployment_name))
                else:
                    self.client = AzureChatOpenAI(
                        api_key=azure_key,
                        azure_endpoint=azure_endpoint,
                        azure_deployment=deployment_name,
                        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-03-15-preview")
                    )
                    logger.info("Azure OpenAI client initialized successfully")
            else:
                logger.debug("Configuring OpenAI client")
                openai_key = os.getenv("OPENAI_API_KEY")
                
                logger.debug(f"OpenAI config - Key present: {bool(openai_key)}")
                if openai_key:
                    logger.debug(f"OpenAI key length: {len(openai_key)}")
                    logger.debug(f"OpenAI key prefix: {openai_key[:10]}...")
                
                if not openai_key:
                    logger.error("OpenAI API key missing in .env. Falling back to default specialties.")
                else:
                    self.client = ChatOpenAI(
                        api_key=openai_key,
                        model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
                    )
                    logger.info("OpenAI client initialized successfully")
                    
        except Exception as e:
            logger.error(f"LLMClient initialization error: {e}", exc_info=True)
            self.client = None

    def get_specialties(self, injury_description: str) -> list:
        logger.debug(f"Getting specialties for injury: {injury_description}")
        
        prompt = (
            "You are a medical specialist who recommends the most appropriate medical specialties for treating specific injuries or conditions. "
            "Return only 2-3 specialty names, separated by commas.\n"
            f"Injury description: '{injury_description}'\nSpecialties:"
        )
        
        logger.debug(f"LLM prompt: {prompt}")
        
        if not self.client:
            logger.warning("LLM client not initialized. Returning fallback specialties.")
            fallback_specialties = ["Orthopedics", "Sports Medicine", "Physical Therapy"]
            logger.debug(f"Returning fallback specialties: {fallback_specialties}")
            return fallback_specialties
            
        try:
            logger.info("Making LLM API call for specialty recommendation")
            response = self.client.invoke(prompt)
            content = response.content.strip()
            specialties = [s.strip() for s in content.split(",") if s.strip()]
            
            logger.info(f"LLM response received - Raw: '{content}'")
            logger.info(f"Parsed specialties: {specialties}")
            
            if not specialties:
                raise ValueError("No specialties returned from LLM.")
                
            return specialties
            
        except Exception as e:
            logger.error(f"LLMClient error during API call: {e}", exc_info=True)
            fallback_specialties = ["Orthopedics", "Sports Medicine", "Physical Therapy"]
            logger.info(f"Returning fallback specialties due to error: {fallback_specialties}")
            return fallback_specialties 