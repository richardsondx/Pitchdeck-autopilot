"""
Deck Parser Module - Extract text from PDF and PPTX files with OCR fallback.
"""

import pdfplumber
from pptx import Presentation
import pytesseract
from PIL import Image
from typing import List, Dict, Tuple
import io
import os
import subprocess
import shutil
import tempfile


class SlideContent:
    """Represents content extracted from a single slide/page."""
    
    def __init__(self, slide_number: int, text: str, extraction_method: str = "direct"):
        self.slide_number = slide_number
        self.text = text
        self.extraction_method = extraction_method  # "direct" or "ocr"
    
    def __repr__(self):
        return f"Slide {self.slide_number} ({self.extraction_method}): {len(self.text)} chars"


def _is_mostly_empty(slides: List[SlideContent], min_chars: int = 20, threshold: float = 0.75) -> bool:
    """Check if most slides have minimal extractable text."""
    if not slides:
        return True
    empty = sum(1 for s in slides if len((s.text or "").strip()) < min_chars)
    return (empty / len(slides)) >= threshold


def _convert_pptx_to_pdf(pptx_path: str) -> str | None:
    """Convert PPTX to PDF using LibreOffice if available.
    
    Creates a temporary PDF file that should be cleaned up by the caller.
    
    Returns:
        Path to temporary PDF file, or None if conversion failed
    """
    soffice = shutil.which("soffice")
    if not soffice:
        return None
    
    # Use a temporary directory for conversion
    temp_dir = tempfile.mkdtemp(prefix="deckbrief_")
    
    try:
        subprocess.run(
            [soffice, "--headless", "--convert-to", "pdf:writer_pdf_Export", 
             pptx_path, "--outdir", temp_dir],
            check=True,
            capture_output=True,
            timeout=30
        )
        # Get the expected PDF filename
        base_name = os.path.splitext(os.path.basename(pptx_path))[0]
        pdf_path = os.path.join(temp_dir, base_name + ".pdf")
        return pdf_path if os.path.exists(pdf_path) else None
    except Exception:
        # Clean up temp directory if conversion failed
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass
        return None


def extract_from_pdf(file_path: str) -> Tuple[List[SlideContent], int]:
    """
    Extract text from a PDF file.
    
    Returns:
        Tuple of (list of SlideContent objects, number of OCR-extracted slides)
    """
    slides = []
    ocr_count = 0
    
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                # Try direct text extraction first
                text = page.extract_text()
                
                if text and len(text.strip()) > 50:  # Decent amount of text
                    slides.append(SlideContent(page_num, text, "direct"))
                else:
                    # Try OCR fallback for image-heavy pages
                    try:
                        # Convert page to image
                        img = page.to_image(resolution=150)
                        pil_image = img.original
                        
                        # Perform OCR
                        ocr_text = pytesseract.image_to_string(pil_image)
                        
                        if ocr_text and len(ocr_text.strip()) > 20:
                            slides.append(SlideContent(page_num, ocr_text, "ocr"))
                            ocr_count += 1
                        else:
                            # Even OCR found nothing substantial
                            slides.append(SlideContent(page_num, text or "", "direct"))
                    except Exception as ocr_error:
                        # OCR failed, use whatever text we got
                        slides.append(SlideContent(page_num, text or "", "direct"))
    
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")
    
    return slides, ocr_count


def extract_from_pptx(file_path: str) -> Tuple[List[SlideContent], int]:
    """
    Extract text from a PPTX file.
    
    Returns:
        Tuple of (list of SlideContent objects, number of OCR-extracted slides)
    """
    slides = []
    ocr_count = 0
    
    try:
        prs = Presentation(file_path)
        
        for slide_num, slide in enumerate(prs.slides, start=1):
            text_parts = []
            
            # Extract text from all shapes
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text:
                    text_parts.append(shape.text)
                
                # Handle tables
                if shape.shape_type == 19:  # Table
                    try:
                        table = shape.table
                        for row in table.rows:
                            for cell in row.cells:
                                if cell.text:
                                    text_parts.append(cell.text)
                    except:
                        pass
            
            combined_text = "\n".join(text_parts)
            
            # If we got decent text, use it
            # Change from > 30 to > 10 to accept short slides like "Team"
            if combined_text and len(combined_text.strip()) > 10:
                slides.append(SlideContent(slide_num, combined_text, "direct"))
            else:
                # For PPTX, we could try OCR on slide images, but it's less common
                # For now, just save whatever we have
                slides.append(SlideContent(slide_num, combined_text, "direct"))
    
    except Exception as e:
        raise ValueError(f"Failed to parse PPTX: {str(e)}")
    
    return slides, ocr_count


def parse_deck(file_path: str) -> Tuple[List[SlideContent], int]:
    """
    Parse a deck file (PDF or PPTX) and extract content.
    
    Args:
        file_path: Path to the deck file
    
    Returns:
        Tuple of (list of SlideContent objects, number of OCR-extracted slides)
    
    Raises:
        ValueError: If file format is unsupported or parsing fails
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == ".pdf":
        return extract_from_pdf(file_path)
    elif file_ext in [".pptx", ".ppt"]:
        # Note: python-pptx only supports .pptx, not old .ppt format
        if file_ext == ".ppt":
            raise ValueError("Old .ppt format not supported. Please convert to .pptx first.")
        
        slides, ocr_count = extract_from_pptx(file_path)
        
        # Smart fallback: if PPTX is mostly empty, convert to PDF and re-parse with OCR
        if _is_mostly_empty(slides):
            temp_pdf_path = _convert_pptx_to_pdf(file_path)
            if temp_pdf_path and os.path.exists(temp_pdf_path):
                try:
                    # Re-extract from PDF with OCR support
                    result = extract_from_pdf(temp_pdf_path)
                    return result
                finally:
                    # Clean up temporary PDF and its directory
                    try:
                        temp_dir = os.path.dirname(temp_pdf_path)
                        shutil.rmtree(temp_dir, ignore_errors=True)
                    except:
                        pass
        
        return slides, ocr_count
    else:
        raise ValueError(f"Unsupported file format: {file_ext}. Only .pdf and .pptx are supported.")


def get_full_text(slides: List[SlideContent]) -> str:
    """
    Combine all slide texts into a single document.
    
    Args:
        slides: List of SlideContent objects
    
    Returns:
        Combined text from all slides
    """
    return "\n\n".join([
        f"--- Slide {slide.slide_number} ---\n{slide.text}"
        for slide in slides
        if slide.text.strip()
    ])

