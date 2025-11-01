"""
Unit and integration tests for deck_parser module.
"""

import pytest
import os
from deckbrief.deck_parser import (
    parse_deck,
    extract_from_pdf,
    extract_from_pptx,
    get_full_text,
    SlideContent,
)


class TestParseDeck:
    """Test the main parse_deck function."""
    
    def test_parse_pdf(self, sample_pdf_path):
        """Test parsing a PDF file."""
        slides, ocr_count = parse_deck(sample_pdf_path)
        
        assert len(slides) > 0
        assert isinstance(slides[0], SlideContent)
        assert ocr_count >= 0
    
    def test_parse_pptx(self, sample_pptx_path):
        """Test parsing a PPTX file."""
        slides, ocr_count = parse_deck(sample_pptx_path)
        
        assert len(slides) > 0
        assert isinstance(slides[0], SlideContent)
    
    def test_file_not_found(self):
        """Test error handling for missing file."""
        with pytest.raises(ValueError, match="File not found"):
            parse_deck("/nonexistent/file.pdf")
    
    def test_unsupported_format(self, temp_dir):
        """Test error handling for unsupported file formats."""
        txt_file = os.path.join(temp_dir, "test.txt")
        with open(txt_file, 'w') as f:
            f.write("Test")
        
        with pytest.raises(ValueError, match="Unsupported file format"):
            parse_deck(txt_file)
    
    def test_old_ppt_format(self, temp_dir):
        """Test error handling for old .ppt format."""
        ppt_file = os.path.join(temp_dir, "test.ppt")
        with open(ppt_file, 'w') as f:
            f.write("Fake ppt")
        
        with pytest.raises(ValueError, match="not supported"):
            parse_deck(ppt_file)


class TestExtractFromPDF:
    """Test PDF extraction."""
    
    def test_extract_text_from_pdf(self, sample_pdf_path):
        """Test extracting text from PDF."""
        slides, ocr_count = extract_from_pdf(sample_pdf_path)
        
        assert len(slides) > 0
        
        # Check content
        full_text = " ".join([s.text for s in slides])
        assert "TestCo" in full_text or "Robotics" in full_text
    
    def test_slide_numbering(self, sample_pdf_path):
        """Test that slides are numbered correctly."""
        slides, _ = extract_from_pdf(sample_pdf_path)
        
        for i, slide in enumerate(slides, start=1):
            assert slide.slide_number == i
    
    def test_extraction_method_tracking(self, sample_pdf_path):
        """Test that extraction method is tracked."""
        slides, _ = extract_from_pdf(sample_pdf_path)
        
        for slide in slides:
            assert slide.extraction_method in ["direct", "ocr"]
    
    def test_corrupted_pdf(self, corrupted_file_path):
        """Test handling of corrupted PDF."""
        with pytest.raises(ValueError):
            extract_from_pdf(corrupted_file_path)
    
    def test_empty_pdf(self, empty_pdf_path):
        """Test handling of empty PDF."""
        slides, _ = extract_from_pdf(empty_pdf_path)
        
        # Should return at least one slide (even if empty)
        assert len(slides) >= 1


class TestExtractFromPPTX:
    """Test PPTX extraction."""
    
    def test_extract_text_from_pptx(self, sample_pptx_path):
        """Test extracting text from PPTX."""
        slides, _ = extract_from_pptx(sample_pptx_path)
        
        assert len(slides) > 0
        
        # Check content
        full_text = " ".join([s.text for s in slides])
        assert "TestCo" in full_text or "Robotics" in full_text
    
    def test_pptx_slide_count(self, sample_pptx_path):
        """Test that all slides are extracted."""
        slides, _ = extract_from_pptx(sample_pptx_path)
        
        # We created 3 slides in the fixture
        assert len(slides) == 3
    
    def test_pptx_corrupted(self, temp_dir):
        """Test handling of corrupted PPTX."""
        fake_pptx = os.path.join(temp_dir, "fake.pptx")
        with open(fake_pptx, 'w') as f:
            f.write("Not a real PPTX file")
        
        with pytest.raises(ValueError):
            extract_from_pptx(fake_pptx)


class TestGetFullText:
    """Test full text compilation."""
    
    def test_combine_slides(self):
        """Test combining multiple slides into full text."""
        slides = [
            SlideContent(1, "First slide text", "direct"),
            SlideContent(2, "Second slide text", "direct"),
            SlideContent(3, "Third slide text", "ocr"),
        ]
        
        full_text = get_full_text(slides)
        
        assert "First slide text" in full_text
        assert "Second slide text" in full_text
        assert "Third slide text" in full_text
        assert "--- Slide 1 ---" in full_text
        assert "--- Slide 2 ---" in full_text
    
    def test_skip_empty_slides(self):
        """Test that empty slides are skipped."""
        slides = [
            SlideContent(1, "Content here", "direct"),
            SlideContent(2, "   ", "direct"),  # Only whitespace
            SlideContent(3, "", "direct"),  # Empty
            SlideContent(4, "More content", "direct"),
        ]
        
        full_text = get_full_text(slides)
        
        assert "Content here" in full_text
        assert "More content" in full_text
        # Empty slides should not appear - each non-empty slide has "---" twice (before and after slide number)
        assert full_text.count("--- Slide 1 ---") == 1
        assert full_text.count("--- Slide 4 ---") == 1
        # Whitespace and empty slides should not appear
        assert "--- Slide 2 ---" not in full_text
        assert "--- Slide 3 ---" not in full_text


class TestSlideContent:
    """Test SlideContent class."""
    
    def test_create_slide_content(self):
        """Test creating SlideContent object."""
        slide = SlideContent(1, "Test text", "direct")
        
        assert slide.slide_number == 1
        assert slide.text == "Test text"
        assert slide.extraction_method == "direct"
    
    def test_slide_content_repr(self):
        """Test string representation."""
        slide = SlideContent(5, "Some text here", "ocr")
        repr_str = repr(slide)
        
        assert "5" in repr_str
        assert "ocr" in repr_str
    
    def test_slide_content_defaults(self):
        """Test default extraction method."""
        slide = SlideContent(1, "Test")
        
        assert slide.extraction_method == "direct"


@pytest.mark.integration
class TestRealFileExtraction:
    """Integration tests with real files."""
    
    def test_pdf_with_actual_content(self, sample_pdf_path):
        """Test extracting from PDF with known content."""
        slides, _ = parse_deck(sample_pdf_path)
        full_text = get_full_text(slides)
        
        # Should contain some of our test content
        assert len(full_text) > 50  # At least some content
        assert "TestCo" in full_text or "Robotics" in full_text or "Problem" in full_text
    
    def test_pptx_with_actual_content(self, sample_pptx_path):
        """Test extracting from PPTX with known content."""
        slides, _ = parse_deck(sample_pptx_path)
        full_text = get_full_text(slides)
        
        assert len(full_text) > 30
        assert "TestCo" in full_text or "Robotics" in full_text

