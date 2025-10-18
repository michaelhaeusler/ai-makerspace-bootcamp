"""PDF processing service for extracting and chunking text from German insurance policies."""

import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List

import tiktoken
import pypdf
import pymupdf as fitz
from app.core.config import PDFProcessingConfig


class PDFProcessor:
    """Handles PDF text extraction and chunking for German insurance policies."""
    
    def __init__(self, config: PDFProcessingConfig):
        """Initialize PDF processor with configuration."""
        self.config = config
        self.tokenizer = tiktoken.get_encoding(config.encoding_type)
    
    def extract_text(self, pdf_path: str) -> List[Dict]:
        """
        Extract text from PDF with page information.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries with page number and text content
        """
        text_data = []
        
        try:
            # Try pymupdf first (better for complex PDFs)
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                if text.strip():  # Only add non-empty pages
                    text_data.append({
                        "page": page_num + 1,
                        "text": text.strip()
                    })
            doc.close()
            
        except Exception:
            # Fallback to pypdf if pymupdf fails
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    text = page.extract_text()
                    if text.strip():  # Only add non-empty pages
                        text_data.append({
                            "page": page_num + 1,
                            "text": text.strip()
                        })
        
        return text_data
    
    def chunk_text(self, text_data: List[Dict], filename: str) -> List[Dict]:
        """
        Split text into semantic chunks with overlap.
        
        Args:
            text_data: List of page dictionaries with text
            filename: Original filename for metadata
            
        Returns:
            List of chunk dictionaries with metadata
        """
        chunks = []
        current_chunk = ""
        current_pages = []
        current_tokens = 0
        chunk_id = 0
        
        for page_data in text_data:
            page_text = page_data["text"]
            page_num = page_data["page"]
            
            # Tokenize the page text
            page_tokens = self.tokenizer.encode(page_text)
            
            # If single page is too large, split it
            if len(page_tokens) > self.config.chunk_size:
                # Split large page into smaller chunks
                for i in range(0, len(page_tokens), self.config.chunk_size - self.config.overlap_size):
                    chunk_tokens = page_tokens[i:i + self.config.chunk_size]
                    chunk_text = self.tokenizer.decode(chunk_tokens)
                    
                    chunks.append({
                        "chunk_id": f"{filename}_{chunk_id}",
                        "text": chunk_text,
                        "page": page_num,
                        "filename": filename,
                        "upload_date": datetime.now().isoformat(),
                        "token_count": len(chunk_tokens)
                    })
                    chunk_id += 1
            else:
                # Add to current chunk
                if current_tokens + len(page_tokens) > self.config.chunk_size:
                    # Save current chunk
                    if current_chunk.strip():
                        chunks.append({
                            "chunk_id": f"{filename}_{chunk_id}",
                            "text": current_chunk.strip(),
                            "page": min(current_pages) if current_pages else 1,
                            "filename": filename,
                            "upload_date": datetime.now().isoformat(),
                            "token_count": current_tokens
                        })
                        chunk_id += 1
                    
                    # Start new chunk with overlap
                    overlap_tokens = self.tokenizer.encode(current_chunk)[-self.config.overlap_size:]
                    overlap_text = self.tokenizer.decode(overlap_tokens)
                    current_chunk = overlap_text + " " + page_text
                    current_pages = [page_num]
                    current_tokens = len(self.tokenizer.encode(current_chunk))
                else:
                    # Add to current chunk
                    if current_chunk:
                        current_chunk += " " + page_text
                    else:
                        current_chunk = page_text
                    current_pages.append(page_num)
                    current_tokens += len(page_tokens)
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append({
                "chunk_id": f"{filename}_{chunk_id}",
                "text": current_chunk.strip(),
                "page": min(current_pages) if current_pages else 1,
                "filename": filename,
                "upload_date": datetime.now().isoformat(),
                "token_count": current_tokens
            })
        
        return chunks
    
    def process_pdf(self, pdf_path: str, filename: str) -> Dict:
        """
        Main method: extract text and chunk a PDF.
        
        Args:
            pdf_path: Path to the PDF file
            filename: Original filename
            
        Returns:
            Dictionary with chunks, total pages, and total chunks
        """
        # Extract text with page information
        text_data = self.extract_text(pdf_path)
        
        if not text_data:
            raise ValueError("No text could be extracted from the PDF")
        
        # Chunk the text
        chunks = self.chunk_text(text_data, filename)
        
        return {
            "chunks": chunks,
            "total_pages": len(text_data),
            "total_chunks": len(chunks),
            "filename": filename,
            "processing_date": datetime.now().isoformat()
        }
