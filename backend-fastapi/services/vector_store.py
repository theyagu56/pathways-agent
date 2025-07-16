import os
from utils.logger import get_logger
from typing import List

logger = get_logger(__name__)

class VectorStore:
    def __init__(self):
        logger.debug("Initializing VectorStore")
        self.use_faiss = os.getenv("USE_FAISS", "true").lower() == "true"
        self.embeddings = None
        self.store = None
        
        logger.info(f"Vector Store Configuration - Use FAISS: {self.use_faiss}")
        
        if self.use_faiss:
            try:
                logger.debug("Attempting to import FAISS and LangChain Community")
                from langchain_community.vectorstores import FAISS
                from langchain_community.embeddings import OpenAIEmbeddings
                self.embeddings = OpenAIEmbeddings()
                self.store = FAISS
                logger.info("FAISS vector store initialized successfully")
            except ImportError as e:
                logger.error("FAISS or LangChain Community not installed. Please install them for local vector search.", exc_info=True)
            except Exception as e:
                logger.error(f"VectorStore FAISS initialization error: {e}", exc_info=True)
        else:
            logger.info("Azure Cognitive Search integration not implemented yet.")

    def embed_and_search(self, documents: List[str], query: str, top_k: int = 3) -> List[int]:
        logger.debug(f"Performing vector search - Documents: {len(documents)}, Query: '{query}', Top-K: {top_k}")
        
        if self.use_faiss and self.store and self.embeddings:
            try:
                logger.info("Using FAISS for vector search")
                # Placeholder: actual FAISS usage would require persistent index and more setup.
                result = list(range(min(top_k, len(documents))))
                logger.debug(f"FAISS search completed - Results: {result}")
                return result
            except Exception as e:
                logger.error(f"VectorStore FAISS search error: {e}. Returning default indices.", exc_info=True)
                result = list(range(min(top_k, len(documents))))
                logger.debug(f"Returning default indices due to error: {result}")
                return result
        else:
            logger.warning("VectorStore not initialized or not using FAISS. Returning default indices.")
            result = list(range(min(top_k, len(documents))))
            logger.debug(f"Returning default indices: {result}")
            return result 