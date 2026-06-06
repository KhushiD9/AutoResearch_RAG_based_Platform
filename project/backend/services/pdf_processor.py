import httpx
import PyPDF2
import pdfplumber
import io
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    def __init__(self):
        self.chunk_size = 1000
        self.chunk_overlap = 200
    
    async def download_pdf(self, url: str) -> bytes:
        """Download PDF from URL"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=60.0, follow_redirects=True)
                if response.status_code == 200:
                    return response.content
                else:
                    logger.error(f"Failed to download PDF: {response.status_code}")
                    return None
        except Exception as e:
            logger.error(f"Error downloading PDF: {str(e)}")
            return None
    
    def extract_text_pypdf2(self, pdf_content: bytes) -> str:
        """Extract text using PyPDF2"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text with PyPDF2: {str(e)}")
            return ""
    
    def extract_text_pdfplumber(self, pdf_content: bytes) -> str:
        """Extract text using pdfplumber (fallback method)"""
        try:
            pdf_file = io.BytesIO(pdf_content)
            text = ""
            
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            
            return text.strip()
        except Exception as e:
            logger.error(f"Error extracting text with pdfplumber: {str(e)}")
            return ""
    
    def extract_text(self, pdf_content: bytes) -> str:
        """Extract text from PDF with fallback methods"""
        text = self.extract_text_pypdf2(pdf_content)
        
        if not text or len(text) < 100:
            text = self.extract_text_pdfplumber(pdf_content)
        
        return text
    
    def chunk_text(self, text: str) -> List[Dict[str, str]]:
        """Split text into overlapping chunks"""
        chunks = []
        
        # Split by paragraphs first
        paragraphs = text.split("\n\n")
        
        current_chunk = ""
        chunk_id = 0
        
        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue
            
            if len(current_chunk) + len(paragraph) < self.chunk_size:
                current_chunk += paragraph + "\n\n"
            else:
                if current_chunk:
                    chunks.append({
                        "chunk_id": chunk_id,
                        "text": current_chunk.strip()
                    })
                    chunk_id += 1
                    
                    # Add overlap
                    words = current_chunk.split()
                    overlap_text = " ".join(words[-self.chunk_overlap:]) if len(words) > self.chunk_overlap else current_chunk
                    current_chunk = overlap_text + "\n\n" + paragraph + "\n\n"
                else:
                    current_chunk = paragraph + "\n\n"
        
        # Add the last chunk
        if current_chunk:
            chunks.append({
                "chunk_id": chunk_id,
                "text": current_chunk.strip()
            })
        
        return chunks
    
    async def process_pdf(self, pdf_url: str) -> Dict:
        """Download PDF, extract text, and chunk it"""
        pdf_content = await self.download_pdf(pdf_url)
        
        if not pdf_content:
            return {
                "success": False,
                "error": "Failed to download PDF"
            }
        
        text = self.extract_text(pdf_content)
        
        if not text:
            return {
                "success": False,
                "error": "Failed to extract text from PDF"
            }
        
        chunks = self.chunk_text(text)
        
        return {
            "success": True,
            "text": text,
            "chunks": chunks,
            "chunk_count": len(chunks)
        }
