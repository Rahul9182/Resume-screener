"""
PDF text extraction module
Supports both digital and scanned PDFs
"""

import io
try:
    import PyPDF2
    import pdfplumber
except ImportError:
    pass

def extract_text_from_pdf(file_content):
    """
    Extract text from PDF file, fallback to OCR if needed.
    """
    text = ""
    try:
        # Try pdfplumber first (digital PDFs)
        try:
            with pdfplumber.open(io.BytesIO(file_content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            if text and len(text.strip()) > 50:
                print("[INFO] Used pdfplumber for PDF extraction")

                print("======PDF Text Extraction=====>",text)
                return text
        except Exception as e:
            print(f"[WARN] pdfplumber extraction error: {e}")
        # Fallback to PyPDF2
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            if text and len(text.strip()) > 50:
                print("[INFO] Used PyPDF2 for PDF extraction")

                print("======PDF Text Extraction=====>",text)
                return text
        except Exception as e:
            print(f"[WARN] PyPDF2 extraction error: {e}")
        # Fallback to OCR if too short/empty
        if len(text.strip()) < 50:
            print("[INFO] Falling back to OCR extraction for likely scanned PDF...")
            ocr_text = extract_text_with_ocr(file_content)
            if ocr_text and len(ocr_text.strip()) > 20:
                return ocr_text
        
        print("======PDF Text Extraction=====>",text)

        return text
    except Exception as e:
        print(f"Error extracting text from PDF: {str(e)}")
        return ""

def extract_text_with_ocr(file_content):
    """
    Extract text from scanned PDF using OCR
    Requires: pytesseract and PIL
    """
    try:
        from pdf2image import convert_from_bytes
        import pytesseract
        images = convert_from_bytes(file_content)
        text = ""
        for image in images:
            page_text = pytesseract.image_to_string(image)
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        print(f"OCR extraction failed: {str(e)}")
        return ""