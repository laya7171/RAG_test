from pypdf import PdfReader
import io


def extract_text_from_pdf(file_bytes: bytes, filename: str) -> str:
    if filename.endswith('.pdf'):
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    return file_bytes.decode('utf-8')