from typing import List, Dict
import logging
from .paper_discovery import PaperDiscoveryService
from .pdf_processor import PDFProcessor
from .embeddings import EmbeddingService
from .vector_store import VectorStore
from .llm_service import LLMService

logger = logging.getLogger(__name__)


class RAGPipeline:
    """
    Full RAG pipeline:
      1. Discover papers (Semantic Scholar + arXiv)
      2. Download + parse PDFs
      3. Chunk text
      4. Embed chunks with sentence-transformers (local, free)
      5. Store in ChromaDB
      6. Query: embed query -> retrieve chunks -> generate answer with Claude
    """

    def __init__(self, provider: str = "anthropic"):
        self.paper_discovery = PaperDiscoveryService()
        self.pdf_processor   = PDFProcessor()
        self.embedding_svc   = EmbeddingService(provider="local")
        self.vector_store    = VectorStore()
        self.llm_service     = LLMService(provider="anthropic")

    # ── INDEX ──────────────────────────────────────────────────────────────

    async def index_papers(self, topic: str, limit: int = 5) -> Dict:
        logger.info(f"Pipeline: indexing topic='{topic}' limit={limit}")

        papers = await self.paper_discovery.search_papers(topic, limit)
        if not papers:
            return {"success": False, "error": "No papers found for this topic.", "papers_processed": 0}

        collection_name = "topic_" + topic.replace(" ", "_").lower()[:60]
        processed = []

        for paper in papers:
            try:
                if not paper.get("pdf_url"):
                    logger.warning(f"No PDF URL: {paper['title']}")
                    continue

                pdf_result = await self.pdf_processor.process_pdf(paper["pdf_url"])
                if not pdf_result["success"]:
                    logger.warning(f"PDF processing failed: {paper['title']}")
                    continue

                chunks = pdf_result["chunks"]
                if not chunks:
                    continue

                texts      = [c["text"] for c in chunks]
                embeddings = await self.embedding_svc.generate_embeddings(texts)
                if not embeddings:
                    continue

                metadatas = [
                    {
                        "paper_id":   str(paper["id"]),
                        "title":      paper["title"][:200],
                        "authors":    ", ".join(paper["authors"][:3]),
                        "year":       str(paper.get("year", "")),
                        "chunk_id":   str(c["chunk_id"]),
                        "source":     paper.get("source", ""),
                    }
                    for c in chunks
                ]
                ids = [f"{paper['id']}_chunk_{c['chunk_id']}" for c in chunks]

                self.vector_store.add_documents(
                    collection_name=collection_name,
                    documents=texts,
                    metadatas=metadatas,
                    ids=ids,
                    embeddings=embeddings,
                )
                processed.append({
                    "paper_id":    str(paper["id"]),
                    "title":       paper["title"],
                    "chunks_count": len(chunks),
                })
                logger.info(f"Indexed: {paper['title']} ({len(chunks)} chunks)")

            except Exception as e:
                logger.error(f"Error processing '{paper.get('title', '?')}': {e}")
                continue

        return {
            "success":          True,
            "collection_name":  collection_name,
            "papers_found":     len(papers),
            "papers_processed": len(processed),
            "processed_papers": processed,
        }

    # ── QUERY ──────────────────────────────────────────────────────────────

    async def query(
        self,
        collection_name: str,
        question: str,
        n_results: int = 5,
        mode: str = "standard",
    ) -> Dict:
        logger.info(f"Pipeline: query collection='{collection_name}' mode={mode}")

        query_emb = await self.embedding_svc.generate_query_embedding(question)
        if not query_emb:
            return {"success": False, "error": "Failed to embed query."}

        results = self.vector_store.query_documents(
            collection_name=collection_name,
            query_embeddings=[query_emb],
            n_results=n_results,
        )

        docs  = results.get("documents", [[]])[0]
        metas = results.get("metadatas",  [[]])[0]

        if not docs:
            return {"success": False, "error": "No relevant documents found in the collection."}

        context_chunks = [{"text": d, "metadata": m} for d, m in zip(docs, metas)]

        answer = await self.llm_service.generate_answer(question, context_chunks, mode)

        return {
            "success":      True,
            "answer":       answer,
            "sources":      context_chunks,
            "sources_count": len(context_chunks),
        }
