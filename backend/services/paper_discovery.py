import asyncio
import httpx
import arxiv
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class PaperDiscoveryService:
    def __init__(self):
        self.semantic_scholar_base = "https://api.semanticscholar.org/graph/v1"
        self.rate_limited = False
        
    async def search_semantic_scholar(self, query: str, limit: int = 10) -> List[Dict]:
        """Search papers using Semantic Scholar API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.semantic_scholar_base}/paper/search",
                    params={
                        "query": query,
                        "limit": limit,
                        "fields": "paperId,title,abstract,year,authors,openAccessPdf,citationCount,url"
                    },
                    headers={"User-Agent": "ResearchPaperAssistant/1.0"},
                    timeout=30.0
                )
                
                if response.status_code == 429:
                    self.rate_limited = True
                    logger.error("Semantic Scholar API error: 429")
                    return []

                if response.status_code == 200:
                    data = response.json()
                    papers = []
                    
                    for paper in data.get("data", []):
                        pdf_url = (paper.get("openAccessPdf") or {}).get("url")
                        abstract = paper.get("abstract") or ""
                        if pdf_url or abstract:
                            papers.append({
                                "id": paper.get("paperId"),
                                "title": paper.get("title"),
                                "abstract": abstract,
                                "year": paper.get("year"),
                                "authors": [author.get("name") for author in paper.get("authors", [])],
                                "pdf_url": pdf_url,
                                "citation_count": paper.get("citationCount", 0),
                                "source_url": paper.get("url"),
                                "source": "semantic_scholar"
                            })
                    
                    return papers
                else:
                    logger.error(f"Semantic Scholar API error: {response.status_code}")
                    return []
                    
        except Exception as e:
            logger.error(f"Error searching Semantic Scholar: {str(e)}")
            return []
    
    async def search_arxiv(self, query: str, limit: int = 10) -> List[Dict]:
        """Search papers using arXiv API"""
        try:
            client = arxiv.Client(
                page_size=min(limit, 10),
                delay_seconds=3.0,
                num_retries=3
            )
            search = arxiv.Search(
                query=query,
                max_results=limit,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            papers = []
            for result in client.results(search):
                papers.append({
                    "id": result.entry_id.split("/")[-1],
                    "title": result.title,
                    "abstract": result.summary,
                    "year": result.published.year,
                    "authors": [author.name for author in result.authors],
                    "pdf_url": result.pdf_url,
                    "citation_count": 0,
                    "source_url": result.entry_id,
                    "source": "arxiv"
                })
            
            return papers
            
        except Exception as e:
            if "429" in str(e):
                self.rate_limited = True
            logger.error(f"Error searching arXiv: {str(e)}")
            return []
    
    async def search_papers(self, query: str, limit: int = 10, sources: List[str] = None) -> List[Dict]:
        """Search papers from multiple sources"""
        if sources is None:
            sources = ["semantic_scholar", "arxiv"]
        
        all_papers = []
        
        if "semantic_scholar" in sources:
            ss_papers = await self.search_semantic_scholar(query, limit)
            all_papers.extend(ss_papers)
            await asyncio.sleep(1)
        
        if "arxiv" in sources:
            arxiv_papers = await self.search_arxiv(query, limit)
            all_papers.extend(arxiv_papers)
        
        # Remove duplicates based on title similarity
        unique_papers = self._remove_duplicates(all_papers)
        
        return unique_papers[:limit]
    
    def _remove_duplicates(self, papers: List[Dict]) -> List[Dict]:
        """Remove duplicate papers based on title similarity"""
        seen_titles = set()
        unique_papers = []
        
        for paper in papers:
            title_normalized = paper["title"].lower().strip()
            if title_normalized not in seen_titles:
                seen_titles.add(title_normalized)
                unique_papers.append(paper)
        
        return unique_papers
