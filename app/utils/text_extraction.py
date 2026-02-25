from pypdf import PdfReader
import io
from typing import Union


def extract_text_from_pdf(file_bytes: bytes, filename: str) -> str:
    if not filename:
        raise ValueError("Filename cannot be empty")
    
    if not file_bytes:
        raise ValueError("File bytes cannot be empty")
    
    # Handle PDF files
    if filename.lower().endswith('.pdf'):
        try:
            reader = PdfReader(io.BytesIO(file_bytes))
            text_parts = []
            
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
            
            if not text_parts:
                raise ValueError("No text content could be extracted from the PDF")
            
            return "\n".join(text_parts)
        
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}") from e
    
    # Handle TXT files
    elif filename.lower().endswith('.txt'):
        try:
            # Try UTF-8 first, fallback to Latin-1 if that fails
            try:
                return file_bytes.decode('utf-8')
            except UnicodeDecodeError:
                return file_bytes.decode('latin-1')
        
        except Exception as e:
            raise Exception(f"Failed to decode text file: {str(e)}") from e
    
    else:
        raise ValueError(f"Unsupported file format: {filename}. Only .pdf and .txt files are supported.")