import google.generativeai as genai
from openai import OpenAI
from typing import List
import logging
from config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        
        if provider == "gemini":
            genai.configure(api_key=settings.GEMINI_API_KEY)
        elif provider == "openai":
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts"""
        if self.provider == "gemini":
            return await self._generate_gemini_embeddings(texts)
        elif self.provider == "openai":
            return await self._generate_openai_embeddings(texts)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")
    
    async def _generate_gemini_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using Gemini"""
        try:
            embeddings = []
            
            for text in texts:
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document"
                )
                embeddings.append(result['embedding'])
            
            return embeddings
        except Exception as e:
            logger.error(f"Error generating Gemini embeddings: {str(e)}")
            return []
    
    async def _generate_openai_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings using OpenAI"""
        try:
            response = self.openai_client.embeddings.create(
                model="text-embedding-ada-002",
                input=texts
            )
            
            embeddings = [item.embedding for item in response.data]
            return embeddings
        except Exception as e:
            logger.error(f"Error generating OpenAI embeddings: {str(e)}")
            return []
    
    async def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a query"""
        if self.provider == "gemini":
            try:
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=query,
                    task_type="retrieval_query"
                )
                return result['embedding']
            except Exception as e:
                logger.error(f"Error generating Gemini query embedding: {str(e)}")
                return []
        elif self.provider == "openai":
            embeddings = await self._generate_openai_embeddings([query])
            return embeddings[0] if embeddings else []
