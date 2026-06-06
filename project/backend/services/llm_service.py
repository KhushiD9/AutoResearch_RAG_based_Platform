import google.generativeai as genai
from typing import List, Dict
import logging
from config import settings

logger = logging.getLogger(__name__)

class LLMService:
    MODEL = "gemini-1.5-flash"  # free tier, fast

    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.MODEL)

    async def generate_answer(self, question: str, context_chunks: List[Dict], mode: str = "standard") -> str:
        dispatch = {
            "compare":           self._build_comparison_prompt,
            "literature_review": self._build_literature_review_prompt,
            "research_gaps":     self._build_research_gaps_prompt,
        }
        build_fn = dispatch.get(mode, self._build_standard_prompt)
        prompt = build_fn(question, context_chunks)
        return self._call(prompt)

    def _context_block(self, chunks: List[Dict]) -> str:
        parts = []
        for i, chunk in enumerate(chunks, 1):
            title = chunk["metadata"].get("title", "Unknown")
            parts.append(f"[Source {i}] {title}\n{chunk['text']}")
        return "\n\n".join(parts)

    def _build_standard_prompt(self, question: str, chunks: List[Dict]) -> str:
        return f"""You are a rigorous research assistant analysing scientific papers.

CONTEXT FROM PAPERS:
{self._context_block(chunks)}

QUESTION: {question}

Instructions:
- Base your answer strictly on the context above.
- Cite sources as [Source N] inline.
- If the context is insufficient, say so clearly.
- Use precise, domain-appropriate language.
- Do not use emojis.

Answer:"""

    def _build_comparison_prompt(self, question: str, chunks: List[Dict]) -> str:
        return f"""You are a research assistant comparing scientific papers.

PAPERS:
{self._context_block(chunks)}

COMPARISON REQUEST: {question}

Instructions:
- Compare methodologies, findings, and conclusions across papers.
- Structure the comparison with clear headings.
- Highlight key similarities and differences.
- Do not use emojis.

Comparison:"""

    def _build_literature_review_prompt(self, question: str, chunks: List[Dict]) -> str:
        return f"""You are a research assistant writing a formal literature review.

RESEARCH PAPERS:
{self._context_block(chunks)}

TOPIC: {question}

Instructions:
- Write an academic literature review (400-600 words).
- Synthesise themes, trends, and major findings.
- Use formal academic prose. No emojis.

Literature Review:"""

    def _build_research_gaps_prompt(self, question: str, chunks: List[Dict]) -> str:
        return f"""You are a research assistant identifying gaps in scientific literature.

RESEARCH PAPERS:
{self._context_block(chunks)}

TOPIC: {question}

Instructions:
- Identify 4-6 specific research gaps.
- For each: state the limitation, why it matters, suggest a research direction.
- Number each gap. No emojis.

Research Gaps:"""

    def _call(self, prompt: str) -> str:
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini call failed: {e}")
            return f"Error generating response: {str(e)}"