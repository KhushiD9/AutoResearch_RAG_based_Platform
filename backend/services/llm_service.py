import google.generativeai as genai
from openai import OpenAI
from typing import List, Dict
import logging
from config import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self, provider: str = "gemini"):
        self.provider = provider
        
        if provider == "gemini":
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        elif provider == "openai":
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_answer(
        self,
        question: str,
        context_chunks: List[Dict],
        mode: str = "standard"
    ) -> str:
        """Generate an answer based on the question and retrieved context"""
        
        if mode == "compare":
            prompt = self._build_comparison_prompt(question, context_chunks)
        elif mode == "literature_review":
            prompt = self._build_literature_review_prompt(question, context_chunks)
        elif mode == "research_gaps":
            prompt = self._build_research_gaps_prompt(question, context_chunks)
        else:
            prompt = self._build_standard_prompt(question, context_chunks)
        
        if self.provider == "gemini":
            return await self._generate_gemini_response(prompt)
        elif self.provider == "openai":
            return await self._generate_openai_response(prompt)
    
    def _build_standard_prompt(self, question: str, context_chunks: List[Dict]) -> str:
        """Build prompt for standard Q&A"""
        context = "\n\n".join([
            f"Source {i+1} (from {chunk['metadata'].get('title', 'Unknown')}):\n{chunk['text']}"
            for i, chunk in enumerate(context_chunks)
        ])
        
        prompt = f"""You are a research assistant analyzing scientific papers. Answer the following question based on the provided context from research papers.

Context from research papers:
{context}

Question: {question}

Instructions:
- Answer the question based solely on the provided context
- If the context doesn't contain enough information, acknowledge this
- Cite the sources by referring to "Source 1", "Source 2", etc.
- Be concise but thorough
- Use technical language appropriate for the domain

Answer:"""
        
        return prompt
    
    def _build_comparison_prompt(self, question: str, context_chunks: List[Dict]) -> str:
        """Build prompt for paper comparison"""
        context = "\n\n".join([
            f"Paper {i+1}: {chunk['metadata'].get('title', 'Unknown')}\n{chunk['text']}"
            for i, chunk in enumerate(context_chunks)
        ])
        
        prompt = f"""You are a research assistant comparing scientific papers. Compare the papers based on the following question.

Papers to compare:
{context}

Question: {question}

Instructions:
- Compare the methodologies, findings, and conclusions across papers
- Identify similarities and differences
- Highlight strengths and weaknesses of each approach
- Provide a structured comparison

Comparison:"""
        
        return prompt
    
    def _build_literature_review_prompt(self, question: str, context_chunks: List[Dict]) -> str:
        """Build prompt for literature review generation"""
        context = "\n\n".join([
            f"Paper {i+1}: {chunk['metadata'].get('title', 'Unknown')}\n{chunk['text']}"
            for i, chunk in enumerate(context_chunks)
        ])
        
        prompt = f"""You are a research assistant creating a literature review. Synthesize the following research papers into a cohesive literature review.

Research papers:
{context}

Topic: {question}

Instructions:
- Provide an overview of the current state of research
- Identify key themes and trends
- Discuss major findings and their implications
- Organize the review thematically
- Cite specific papers appropriately

Literature Review:"""
        
        return prompt
    
    def _build_research_gaps_prompt(self, question: str, context_chunks: List[Dict]) -> str:
        """Build prompt for research gap identification"""
        context = "\n\n".join([
            f"Paper {i+1}: {chunk['metadata'].get('title', 'Unknown')}\n{chunk['text']}"
            for i, chunk in enumerate(context_chunks)
        ])
        
        prompt = f"""You are a research assistant identifying research gaps. Analyze the following papers to identify gaps in current research.

Research papers:
{context}

Topic: {question}

Instructions:
- Identify what has been well-studied
- Highlight areas that lack sufficient research
- Point out conflicting findings that need resolution
- Suggest potential future research directions
- Be specific about the gaps identified

Research Gaps Analysis:"""
        
        return prompt
    
    async def _generate_gemini_response(self, prompt: str) -> str:
        """Generate response using Gemini"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Error generating Gemini response: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    async def _generate_openai_response(self, prompt: str) -> str:
        """Generate response using OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are a helpful research assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {str(e)}")
            return f"Error generating response: {str(e)}"
