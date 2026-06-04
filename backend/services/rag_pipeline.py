from typing import List, Dict
import logging
from .paper_discovery import PaperDiscoveryService
from .pdf_processor import PDFProcessor
from .embeddings import EmbeddingService
from .vector_store import VectorStore
from .llm_service import LLMService

logger = logging.getLogger(__name__)

class RAGPipeline:
    def __init__(self, provider: str = "gemini"):
        self.paper_discovery = PaperDiscoveryService()
        self.pdf_processor = PDFProcessor()
        self.embedding_service = EmbeddingService(provider)
        self.vector_store = VectorStore()
        self.llm_service = LLMService(provider)
    
    async def index_papers(self, topic: str, limit: int = 5) -> Dict:
        """Complete pipeline: discover, download, process, and index papers"""
        logger.info(f"Starting indexing pipeline for topic: {topic}")
        
        # Step 1: Discover papers
        papers = await self.paper_discovery.search_papers(topic, limit)
        
        if not papers:
            return {
                "success": False,
                "error": "No papers found for the given topic",
                "papers_processed": 0
            }
        
        logger.info(f"Found {len(papers)} papers")
        
        # Step 2: Process each paper
        processed_papers = []
        collection_name = f"topic_{topic.replace(' ', '_').lower()}"
        
        for paper in papers:
            try:
                logger.info(f"Processing paper: {paper['title']}")
                
                if not paper.get('pdf_url'):
                    logger.warning(f"No PDF URL for paper: {paper['title']}")
                    continue
                
                # Download and extract text
                result = await self.pdf_processor.process_pdf(paper['pdf_url'])
                
                if not result['success']:
                    logger.warning(f"Failed to process PDF: {paper['title']}")
                    continue
                
                chunks = result['chunks']
                
                # Generate embeddings
                texts = [chunk['text'] for chunk in chunks]
                embeddings = await self.embedding_service.generate_embeddings(texts)
                
                if not embeddings:
                    logger.warning(f"Failed to generate embeddings for: {paper['title']}")
                    continue
                
                # Prepare metadata
                metadatas = [
                    {
                        "paper_id": paper['id'],
                        "title": paper['title'],
                        "authors": ", ".join(paper['authors'][:3]),
                        "year": paper['year'],
                        "chunk_id": chunk['chunk_id'],
                        "source": paper['source']
                    }
                    for chunk in chunks
                ]
                
                # Generate IDs
                ids = [f"{paper['id']}_chunk_{chunk['chunk_id']}" for chunk in chunks]
                
                # Add to vector store
                self.vector_store.add_documents(
                    collection_name=collection_name,
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids,
                    embeddings=embeddings
                )
                
                processed_papers.append({
                    "paper_id": paper['id'],
                    "title": paper['title'],
                    "chunks_count": len(chunks)
                })
                
                logger.info(f"Successfully processed: {paper['title']}")
                
            except Exception as e:
                logger.error(f"Error processing paper {paper['title']}: {str(e)}")
                continue
        
        return {
            "success": True,
            "collection_name": collection_name,
            "papers_found": len(papers),
            "papers_processed": len(processed_papers),
            "processed_papers": processed_papers
        }
    
    async def query(
        self,
        collection_name: str,
        question: str,
        n_results: int = 5,
        mode: str = "standard"
    ) -> Dict:
        """Query the indexed papers and generate an answer"""
        logger.info(f"Querying collection: {collection_name}")
        
        # Generate query embedding
        query_embedding = await self.embedding_service.generate_query_embedding(question)
        
        if not query_embedding:
            return {
                "success": False,
                "error": "Failed to generate query embedding"
            }
        
        # Retrieve relevant chunks
        results = self.vector_store.query_documents(
            collection_name=collection_name,
            query_embeddings=[query_embedding],
            n_results=n_results
        )
        
        if not results['documents'] or not results['documents'][0]:
            return {
                "success": False,
                "error": "No relevant documents found"
            }
        
        # Prepare context chunks
        context_chunks = [
            {
                "text": doc,
                "metadata": meta
            }
            for doc, meta in zip(results['documents'][0], results['metadatas'][0])
        ]
        
        # Generate answer
        answer = await self.llm_service.generate_answer(question, context_chunks, mode)
        
        return {
            "success": True,
            "answer": answer,
            "sources": context_chunks,
            "sources_count": len(context_chunks)
        }
