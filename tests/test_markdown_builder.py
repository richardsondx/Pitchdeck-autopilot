"""
Unit tests for markdown_builder module.
"""

import pytest
import os
from datetime import datetime
from freezegun import freeze_time
from deckbrief.markdown_builder import (
    build_markdown,
    calculate_confidence,
    sanitize_filename,
    save_markdown,
    save_debug_info,
)
from deckbrief.ai_analyzer import AnalysisResult


class TestBuildMarkdown:
    """Test markdown document building."""
    
    def test_build_basic_markdown(self, sample_analysis_data):
        """Test building markdown from complete analysis data."""
        analysis = AnalysisResult(sample_analysis_data)
        markdown = build_markdown(analysis, slide_count=32, ocr_count=2)
        
        # Check structure
        assert "# Company Brief:" in markdown
        assert sample_analysis_data["Company"] in markdown
        assert "**Deck Parsed:** 32 slides" in markdown
        assert "**OCR Used:** 2 slides" in markdown
        
        # Check sections
        assert "🧩 Problem" in markdown
        assert "🚀 Solution" in markdown
        assert "📈 Traction" in markdown
        assert "👥 Team" in markdown
        assert "🌍 Market" in markdown
        assert "🧱 Moat" in markdown
        assert "⚠️ Risks" in markdown
        
        # Check content
        assert sample_analysis_data["Problem"] in markdown
        assert sample_analysis_data["Solution"] in markdown
    
    def test_build_markdown_without_ocr(self, sample_analysis_data):
        """Test building markdown when no OCR was used."""
        analysis = AnalysisResult(sample_analysis_data)
        markdown = build_markdown(analysis, slide_count=20, ocr_count=0)
        
        assert "**Deck Parsed:** 20 slides" in markdown
        assert "OCR Used" not in markdown
    
    def test_build_markdown_with_tagline(self, sample_analysis_data):
        """Test that tagline is included in output."""
        analysis = AnalysisResult(sample_analysis_data)
        markdown = build_markdown(analysis, slide_count=10)
        
        assert sample_analysis_data["Tagline"] in markdown
    
    def test_build_markdown_without_tagline(self, sample_analysis_data):
        """Test markdown building when tagline is missing."""
        data = sample_analysis_data.copy()
        data["Tagline"] = ""
        analysis = AnalysisResult(data)
        markdown = build_markdown(analysis, slide_count=10)
        
        # Should still build successfully
        assert "# Company Brief:" in markdown
    
    @freeze_time("2024-01-15 14:30:00")
    def test_timestamp_in_markdown(self, sample_analysis_data):
        """Test that timestamp is correctly formatted."""
        analysis = AnalysisResult(sample_analysis_data)
        markdown = build_markdown(analysis, slide_count=10)
        
        assert "2024-01-15" in markdown
        assert "14:30" in markdown
    
    def test_sources_section(self, sample_analysis_data):
        """Test that sources are included in output."""
        analysis = AnalysisResult(sample_analysis_data)
        markdown = build_markdown(analysis, slide_count=10)
        
        assert "📚 Sources" in markdown
        assert "Slide 3" in markdown
        assert "Slide 12" in markdown
    
    def test_empty_sections_omitted(self, sample_analysis_data):
        """Test that empty sections are omitted."""
        data = sample_analysis_data.copy()
        data["Traction"] = ""
        data["Market"] = ""
        analysis = AnalysisResult(data)
        markdown = build_markdown(analysis, slide_count=10)
        
        # Empty sections should not appear
        lines = markdown.split('\n')
        traction_headers = [line for line in lines if "📈 Traction" in line]
        # If Traction is empty, it should not have content section
        assert "📈 Traction" not in markdown or data["Traction"] in markdown


class TestCalculateConfidence:
    """Test confidence score calculation."""
    
    def test_full_analysis_high_confidence(self, sample_analysis_data):
        """Test confidence with complete analysis."""
        analysis = AnalysisResult(sample_analysis_data)
        confidence = calculate_confidence(analysis)
        
        # Should be high with all fields filled
        assert confidence >= 90
        assert confidence <= 100
    
    def test_partial_analysis_medium_confidence(self, sample_analysis_data):
        """Test confidence with partially filled analysis."""
        data = sample_analysis_data.copy()
        data["Traction"] = ""
        data["Market"] = ""
        data["Moat"] = ""
        analysis = AnalysisResult(data)
        confidence = calculate_confidence(analysis)
        
        # Should be lower
        assert 40 <= confidence < 90
    
    def test_minimal_analysis_low_confidence(self):
        """Test confidence with minimal analysis."""
        data = {
            "Company": "Test",
            "Tagline": "",
            "Problem": "",
            "Solution": "Short",
            "Traction": "",
            "Team": "",
            "Market": "",
            "Moat": "",
            "Risks": "",
            "Sources": []
        }
        analysis = AnalysisResult(data)
        confidence = calculate_confidence(analysis)
        
        # Should be low
        assert confidence < 50
    
    def test_confidence_with_sources_bonus(self, sample_analysis_data):
        """Test that sources provide confidence bonus."""
        # With sources
        analysis_with = AnalysisResult(sample_analysis_data)
        confidence_with = calculate_confidence(analysis_with)
        
        # Without sources
        data_without = sample_analysis_data.copy()
        data_without["Sources"] = []
        analysis_without = AnalysisResult(data_without)
        confidence_without = calculate_confidence(analysis_without)
        
        # With sources should be higher (or equal if already at 100)
        assert confidence_with >= confidence_without
    
    def test_confidence_bounded(self, sample_analysis_data):
        """Test that confidence is always between 0-100."""
        analysis = AnalysisResult(sample_analysis_data)
        confidence = calculate_confidence(analysis)
        
        assert 0 <= confidence <= 100


class TestSanitizeFilename:
    """Test filename sanitization."""
    
    def test_sanitize_normal_name(self):
        """Test sanitizing a normal company name."""
        result = sanitize_filename("Acme Corp")
        assert result == "Acme_Corp"
    
    def test_sanitize_special_characters(self):
        """Test removal of invalid filename characters."""
        result = sanitize_filename("Company: The/Best*One?")
        assert ":" not in result
        assert "/" not in result
        assert "*" not in result
        assert "?" not in result
    
    def test_sanitize_long_name(self):
        """Test truncation of very long names."""
        long_name = "A" * 100
        result = sanitize_filename(long_name)
        assert len(result) <= 50
    
    def test_sanitize_empty_name(self):
        """Test handling of empty name."""
        result = sanitize_filename("")
        assert result == "Company"
    
    def test_sanitize_only_invalid_chars(self):
        """Test name with only invalid characters."""
        result = sanitize_filename("***///:::???")
        assert result == "Company"
    
    def test_sanitize_trailing_dots(self):
        """Test removal of trailing dots."""
        result = sanitize_filename("Company Name...")
        assert not result.endswith(".")
    
    def test_sanitize_unicode(self):
        """Test handling of unicode characters."""
        result = sanitize_filename("Компания 世界")
        # Should produce some safe result
        assert isinstance(result, str)
        assert len(result) > 0


class TestSaveMarkdown:
    """Test markdown file saving."""
    
    def test_save_to_directory(self, temp_dir, sample_analysis_data):
        """Test saving markdown to a directory."""
        analysis = AnalysisResult(sample_analysis_data)
        markdown = build_markdown(analysis, slide_count=10)
        
        output_path = save_markdown(markdown, "TestCo", temp_dir)
        
        assert os.path.exists(output_path)
        assert output_path.endswith("_Brief.md")
        assert "TestCo" in output_path
    
    def test_save_creates_directory(self, temp_dir, sample_analysis_data):
        """Test that save_markdown creates output directory if missing."""
        analysis = AnalysisResult(sample_analysis_data)
        markdown = build_markdown(analysis, slide_count=10)
        
        new_dir = os.path.join(temp_dir, "new_output")
        output_path = save_markdown(markdown, "TestCo", new_dir)
        
        assert os.path.exists(new_dir)
        assert os.path.exists(output_path)
    
    def test_save_duplicate_handling(self, temp_dir, sample_analysis_data):
        """Test handling of duplicate filenames."""
        analysis = AnalysisResult(sample_analysis_data)
        markdown = build_markdown(analysis, slide_count=10)
        
        # Save once
        path1 = save_markdown(markdown, "TestCo", temp_dir)
        
        # Save again with same name
        path2 = save_markdown(markdown, "TestCo", temp_dir)
        
        # Should create different files
        assert path1 != path2
        assert os.path.exists(path1)
        assert os.path.exists(path2)
    
    def test_save_content_integrity(self, temp_dir, sample_analysis_data):
        """Test that saved content matches original."""
        analysis = AnalysisResult(sample_analysis_data)
        markdown = build_markdown(analysis, slide_count=10)
        
        output_path = save_markdown(markdown, "TestCo", temp_dir)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            saved_content = f.read()
        
        assert saved_content == markdown
    
    def test_save_utf8_encoding(self, temp_dir):
        """Test that files are saved with UTF-8 encoding."""
        markdown = "# Test\n\nUnicode: 世界 мир"
        output_path = save_markdown(markdown, "Unicode_Test", temp_dir)
        
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "世界" in content
        assert "мир" in content


class TestSaveDebugInfo:
    """Test debug information saving."""
    
    def test_save_debug_files(self, temp_dir):
        """Test saving debug information."""
        raw_text = "This is raw extracted text"
        raw_response = '{"Company": "Test"}'
        
        debug_dir = os.path.join(temp_dir, "debug")
        save_debug_info(raw_text, raw_response, debug_dir)
        
        assert os.path.exists(debug_dir)
        
        # Check files were created
        files = os.listdir(debug_dir)
        assert any("extraction_" in f for f in files)
        assert any("api_response_" in f for f in files)
    
    def test_debug_creates_directory(self, temp_dir):
        """Test that debug directory is created if missing."""
        raw_text = "Test"
        raw_response = "Response"
        
        debug_dir = os.path.join(temp_dir, "new_debug")
        save_debug_info(raw_text, raw_response, debug_dir)
        
        assert os.path.exists(debug_dir)
    
    def test_debug_with_empty_response(self, temp_dir):
        """Test debug saving with empty API response."""
        raw_text = "Test"
        raw_response = ""
        
        debug_dir = os.path.join(temp_dir, "debug")
        # Should not raise error
        save_debug_info(raw_text, raw_response, debug_dir)
        
        assert os.path.exists(debug_dir)


@pytest.mark.integration
class TestEndToEndMarkdownGeneration:
    """Integration tests for complete markdown generation flow."""
    
    def test_complete_flow(self, temp_dir, sample_analysis_data):
        """Test the complete markdown generation flow."""
        # Create analysis
        analysis = AnalysisResult(sample_analysis_data)
        
        # Build markdown
        markdown = build_markdown(analysis, slide_count=32, ocr_count=2)
        
        # Save markdown
        output_path = save_markdown(markdown, analysis.company, temp_dir)
        
        # Verify file exists and contains expected content
        assert os.path.exists(output_path)
        
        with open(output_path, 'r') as f:
            content = f.read()
        
        assert sample_analysis_data["Company"] in content
        assert sample_analysis_data["Problem"] in content
        assert sample_analysis_data["Solution"] in content
        
        # Calculate confidence
        confidence = calculate_confidence(analysis)
        assert confidence > 0


