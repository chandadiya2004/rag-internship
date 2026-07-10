import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_path):
    """
    Attempts to extract text using pdfplumber. 
    Falls back to OCR if the PDF is scanned/image-based.
    Removes unsupported null bytes to prevent database insertion failures.
    """
    extracted_text = ""
    
    # Method 1: Try native text extraction
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
                
    # Method 2: Fallback to OCR if less than 100 characters were found
    if len(extracted_text.strip()) < 100:
        print("Scanned PDF detected. Falling back to OCR...")
        extracted_text = ""
        images = convert_from_path(pdf_path)
        for image in images:
            extracted_text += pytesseract.image_to_string(image) + "\n"
            
    # --- CRITICAL FIX: Strip PostgreSQL-unsupported null bytes ---
    # This removes the \u0000 hidden characters that crash your database upload
    cleaned_text = extracted_text.replace("\x00", "")
    # -------------------------------------------------------------
            
    return cleaned_text

def get_document_chunks(text):
    """Breaks the extracted text into smaller chunks for the Vector DB."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    return text_splitter.split_text(text)