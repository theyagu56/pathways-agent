import os
from langchain.chat_models import ChatOpenAI, AzureChatOpenAI
import logging

class LLMClient:
    def __init__(self):
        use_azure = os.getenv("USE_AZURE_OPENAI", "false").lower() == "true"
        self.use_azure = use_azure
        self.client = None
        try:
            if use_azure:
                azure_key = os.getenv("AZURE_OPENAI_API_KEY")
                azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
                deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
                if not (azure_key and azure_endpoint and deployment_name):
                    logging.error("Azure OpenAI configuration missing in .env. Falling back to default specialties.")
                else:
                    self.client = AzureChatOpenAI(
                        openai_api_key=azure_key,
                        azure_endpoint=azure_endpoint,
                        deployment_name=deployment_name,
                        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-03-15-preview")
                    )
            else:
                openai_key = os.getenv("OPENAI_API_KEY")
                if not openai_key:
                    logging.error("OpenAI API key missing in .env. Falling back to default specialties.")
                else:
                    self.client = ChatOpenAI(
                        openai_api_key=openai_key,
                        model_name=os.getenv("OPENAI_MODEL", "gpt-4")
                    )
        except Exception as e:
            logging.error(f"LLMClient initialization error: {e}")
            self.client = None

    def get_specialties(self, injury_description: str) -> list:
        prompt = (
            "You are a medical specialist who recommends the most appropriate medical specialties for treating specific injuries or conditions. "
            "Return only 2-3 specialty names, separated by commas.\n"
            f"Injury description: '{injury_description}'\nSpecialties:"
        )
        if not self.client:
            logging.warning("LLM client not initialized. Returning fallback specialties.")
            return ["Orthopedics", "Sports Medicine", "Physical Therapy"]
        try:
            response = self.client([{"role": "user", "content": prompt}])
            content = response.content.strip()
            specialties = [s.strip() for s in content.split(",") if s.strip()]
            if not specialties:
                raise ValueError("No specialties returned from LLM.")
            return specialties
        except Exception as e:
            logging.error(f"LLMClient error: {e}. Returning fallback specialties.")
            return ["Orthopedics", "Sports Medicine", "Physical Therapy"] 