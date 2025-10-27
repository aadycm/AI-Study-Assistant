# pdf_reader.py
import fitz  # PyMuPDF

def extract_text(pdf_path):
    """
    Read a PDF and return its full text.
    """
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def split_into_chunks(text, chunk_size=500):
    """
    Split the text into chunks of ~chunk_size words.
    """
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks
