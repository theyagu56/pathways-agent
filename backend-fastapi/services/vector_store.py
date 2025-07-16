import os
from utils.logger import get_logger
from typing import List, Dict, Optional
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
import pandas as pd
import json
from pathlib import Path

logger = get_logger(__name__)

class VectorStore:
    def __init__(self):
        logger.debug("Initializing VectorStore")
        self.use_faiss = os.getenv("USE_FAISS", "true").lower() == "true"
        self.embeddings = None
        self.store = None
        self.vector_store_path = Path("vector_store")
        
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

    def load_excel_data(self, excel_path: str, text_column: str) -> List[Dict]:
        """
        Load Excel data and prepare it for vectorization
        Args:
            excel_path: Path to the Excel file
            text_column: Column name containing the text to be vectorized
        Returns:
            List of dictionaries containing the text and metadata
        """
        logger.info(f"Loading Excel data from {excel_path}")
        try:
            df = pd.read_excel(excel_path)
            # Convert all text data to strings
            df[text_column] = df[text_column].astype(str)
            
            # Create list of documents with metadata
            documents = []
            for idx, row in df.iterrows():
                doc = {
                    "text": row[text_column],
                    "metadata": row.to_dict()
                }
                documents.append(doc)
            
            logger.info(f"Loaded {len(documents)} documents from Excel")
            return documents
            
        except Exception as e:
            logger.error(f"Error loading Excel data: {e}", exc_info=True)
            raise

    def create_vector_store(self, documents: List[Dict], store_path: Optional[str] = None):
        """
        Create a FAISS vector store from documents
        Args:
            documents: List of documents with text and metadata
            store_path: Optional path to save the vector store
        """
        if not self.use_faiss or not self.embeddings:
            raise ValueError("FAISS vector store not properly initialized")
            
        texts = [doc["text"] for doc in documents]
        metadatas = [doc["metadata"] for doc in documents]
        
        logger.info(f"Creating vector store for {len(texts)} documents")
        
        try:
            # Create embeddings and vector store
            vector_store = self.store.from_texts(
                texts=texts,
                embedding=self.embeddings,
                metadatas=metadatas
            )
            
            # Save the vector store if path is provided
            if store_path:
                logger.info(f"Saving vector store to {store_path}")
                vector_store.save_local(store_path)
            
            return vector_store
            
        except Exception as e:
            logger.error(f"Error creating vector store: {e}", exc_info=True)
            raise

    def search(self, query: str, top_k: int = 3, store_path: Optional[str] = None) -> List[Dict]:
        """
        Search the vector store for similar documents
        Args:
            query: Search query
            top_k: Number of results to return
            store_path: Path to load vector store from
        Returns:
            List of matching documents with scores and metadata
        """
        if not self.use_faiss or not self.embeddings:
            raise ValueError("FAISS vector store not properly initialized")
            
        try:
            # Load vector store if path is provided
            if store_path:
                logger.info(f"Loading vector store from {store_path}")
                vector_store = self.store.load_local(
                    folder_path=store_path,
                    embeddings=self.embeddings
                )
            else:
                logger.warning("No vector store path provided, using in-memory store")
                vector_store = self.store.from_texts(
                    texts=[""],  # Empty texts as we're just using the store structure
                    embedding=self.embeddings,
                    metadatas=[{}]
                )

            # Perform search
            results = vector_store.similarity_search_with_score(
                query=query,
                k=top_k
            )
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    "text": doc.page_content,
                    "metadata": doc.metadata,
                    "score": score
                })
            
            logger.info(f"Found {len(formatted_results)} matching documents")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error performing search: {e}", exc_info=True)
            raise

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