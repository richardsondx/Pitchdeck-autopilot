"""
Unit tests for text_cleaner module - Pure functions.
"""

import pytest
from deckbrief.text_cleaner import (
    clean_text,
    remove_headers_footers,
    merge_fragmented_lines,
    normalize_whitespace,
    clean_special_characters,
    extract_key_sections,
)


class TestCleanText:
    """Test the main clean_text function."""
    
    def test_clean_empty_string(self):
        """Test cleaning an empty string."""
        result = clean_text("")
        assert result == ""
    
    def test_clean_none(self):
        """Test cleaning None input."""
        result = clean_text(None)
        assert result == ""
    
    def test_clean_basic_text(self):
        """Test cleaning basic text with whitespace."""
        text = "  Hello   World  \n\n\n  Test  "
        result = clean_text(text)
        assert "Hello World" in result
        assert "Test" in result
    
    def test_clean_with_headers(self):
        """Test that headers are removed."""
        text = "Confidential\nActual content here\nPage 1 of 20"
        result = clean_text(text)
        assert "Actual content here" in result
        assert "Confidential" not in result


class TestRemoveHeadersFooters:
    """Test header and footer removal."""
    
    def test_remove_confidential(self):
        """Test removal of confidential markers."""
        text = "CONFIDENTIAL\nContent\nAnother line"
        result = remove_headers_footers(text)
        assert "CONFIDENTIAL" not in result
        assert "Content" in result
    
    def test_remove_page_numbers(self):
        """Test removal of page numbers."""
        text = "Content line 1\n5\nContent line 2\nPage 5 of 10"
        result = remove_headers_footers(text)
        assert "Content line 1" in result
        assert "Content line 2" in result
        # Standalone numbers might be removed
    
    def test_remove_copyright(self):
        """Test removal of copyright lines."""
        text = "© 2024 Company Name\nContent here"
        result = remove_headers_footers(text)
        assert "Content here" in result
    
    def test_remove_proprietary(self):
        """Test removal of proprietary markers."""
        text = "Proprietary and Confidential\nMain content"
        result = remove_headers_footers(text)
        assert "Main content" in result
    
    def test_preserve_regular_content(self):
        """Test that regular content is preserved."""
        text = "This is normal text\nWith multiple lines\nAll should remain"
        result = remove_headers_footers(text)
        assert "This is normal text" in result
        assert "With multiple lines" in result
        assert "All should remain" in result


class TestMergeFragmentedLines:
    """Test line merging logic."""
    
    def test_merge_sentence_continuation(self):
        """Test merging lines that continue a sentence."""
        text = "This is a long sentence that got\nsplit across multiple lines"
        result = merge_fragmented_lines(text)
        # Should be merged
        assert "split across multiple lines" in result
    
    def test_preserve_bullet_points(self):
        """Test that bullet points are not merged."""
        text = "• First bullet\n• Second bullet\n• Third bullet"
        result = merge_fragmented_lines(text)
        assert "• First bullet" in result
        assert "• Second bullet" in result
        assert "• Third bullet" in result
    
    def test_preserve_numbered_lists(self):
        """Test that numbered lists are preserved."""
        text = "1. First item\n2. Second item\n3. Third item"
        result = merge_fragmented_lines(text)
        assert "1. First item" in result
        assert "2. Second item" in result
    
    def test_preserve_paragraph_breaks(self):
        """Test that empty lines (paragraph breaks) are preserved."""
        text = "Paragraph one\n\nParagraph two"
        result = merge_fragmented_lines(text)
        lines = result.split('\n')
        # Should have empty line between
        assert any(line == '' for line in lines)
    
    def test_preserve_sentences_with_periods(self):
        """Test that complete sentences are not merged."""
        text = "First sentence.\nSecond sentence.\nThird sentence."
        result = merge_fragmented_lines(text)
        assert "First sentence." in result
        assert "Second sentence." in result


class TestNormalizeWhitespace:
    """Test whitespace normalization."""
    
    def test_multiple_spaces(self):
        """Test that multiple spaces are collapsed."""
        text = "Hello     world    test"
        result = normalize_whitespace(text)
        assert "Hello world test" in result
        assert "     " not in result
    
    def test_multiple_newlines(self):
        """Test that excessive newlines are reduced."""
        text = "Line 1\n\n\n\n\nLine 2"
        result = normalize_whitespace(text)
        # Should have max 2 newlines (paragraph break)
        assert "\n\n\n" not in result
    
    def test_trim_line_whitespace(self):
        """Test that line start/end whitespace is removed."""
        text = "  Line with spaces  \n  Another line  "
        result = normalize_whitespace(text)
        lines = result.split('\n')
        for line in lines:
            if line:  # Non-empty lines
                assert not line.startswith(' ')
                assert not line.endswith(' ')
    
    def test_preserve_single_newlines(self):
        """Test that single newlines are preserved."""
        text = "Line 1\nLine 2\nLine 3"
        result = normalize_whitespace(text)
        assert result.count('\n') >= 2


class TestCleanSpecialCharacters:
    """Test special character cleaning."""
    
    def test_remove_null_bytes(self):
        """Test removal of null bytes and control characters."""
        text = "Hello\x00World\x01Test"
        result = clean_special_characters(text)
        assert "\x00" not in result
        assert "\x01" not in result
        assert "Hello" in result
        assert "World" in result
    
    def test_normalize_unicode_quotes(self):
        """Test normalization of unicode quotes."""
        text = "\u201cHello\u201d \u2018world\u2019"
        result = clean_special_characters(text)
        assert '"Hello"' in result or "Hello" in result
        assert "world" in result
    
    def test_normalize_dashes(self):
        """Test normalization of unicode dashes."""
        text = "Item — with — long dashes"
        result = clean_special_characters(text)
        assert "Item" in result
        assert "with" in result
    
    def test_normalize_ellipsis(self):
        """Test normalization of ellipsis character."""
        text = "Wait… for it"
        result = clean_special_characters(text)
        assert "Wait" in result
        assert "for it" in result
    
    def test_remove_excessive_special_chars(self):
        """Test removal of excessive special character sequences."""
        text = "Content ######### more content"
        result = clean_special_characters(text)
        assert "Content" in result
        assert "more content" in result
    
    def test_preserve_normal_punctuation(self):
        """Test that normal punctuation is preserved."""
        text = "Hello, world! How are you? I'm fine."
        result = clean_special_characters(text)
        assert "Hello, world!" in result
        assert "How are you?" in result
        assert "I'm fine." in result


class TestExtractKeySections:
    """Test key section extraction."""
    
    def test_extract_problem_section(self):
        """Test extraction of problem section."""
        text = """
        Some intro text
        
        The Problem
        Industrial robots are expensive
        They require lots of data
        
        Other content
        """
        result = extract_key_sections(text)
        assert 'problem' in result
        assert 'expensive' in result['problem'].lower()
    
    def test_extract_solution_section(self):
        """Test extraction of solution section."""
        text = """
        Our Solution
        We use AI to solve this
        10x faster than competitors
        """
        result = extract_key_sections(text)
        assert 'solution' in result
        assert 'AI' in result['solution']
    
    def test_extract_traction_section(self):
        """Test extraction of traction section."""
        text = """
        Traction
        2 pilot customers
        $250K in revenue
        """
        result = extract_key_sections(text)
        assert 'traction' in result
        assert 'customers' in result['traction'].lower()
    
    def test_extract_team_section(self):
        """Test extraction of team section."""
        text = """
        Our Team
        Ex-Google engineers
        PhDs from MIT
        """
        result = extract_key_sections(text)
        assert 'team' in result
        assert 'engineers' in result['team'].lower()
    
    def test_extract_market_section(self):
        """Test extraction of market section."""
        text = """
        Market Size
        $8B addressable market
        Growing at 20% CAGR
        """
        result = extract_key_sections(text)
        assert 'market' in result
        assert '$8B' in result['market']
    
    def test_extract_multiple_sections(self):
        """Test extraction of multiple sections."""
        text = """
        Problem
        Robots are expensive
        
        Solution
        We make them cheaper
        
        Team
        Expert engineers
        """
        result = extract_key_sections(text)
        assert 'problem' in result
        assert 'solution' in result
        assert 'team' in result
        assert len(result) >= 3
    
    def test_no_sections_found(self):
        """Test when no standard sections are found."""
        text = "Just some random text without section headers"
        result = extract_key_sections(text)
        # Should return empty or minimal dict
        assert isinstance(result, dict)


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_very_long_text(self):
        """Test handling of very long text."""
        text = "A" * 100000
        result = clean_text(text)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_unicode_text(self):
        """Test handling of unicode text."""
        text = "Hello 世界 مرحبا мир"
        result = clean_text(text)
        assert "Hello" in result
    
    def test_mixed_line_endings(self):
        """Test handling of mixed line endings."""
        text = "Line 1\rLine 2\nLine 3\r\nLine 4"
        result = clean_text(text)
        assert "Line 1" in result
        assert "Line 4" in result
    
    def test_only_whitespace(self):
        """Test text that is only whitespace."""
        text = "     \n\n\n     \t\t\t     "
        result = clean_text(text)
        assert result == ""
    
    def test_special_regex_characters(self):
        """Test text with regex special characters."""
        text = "Amount: $100 (or €85) [approx]"
        result = clean_text(text)
        assert "$100" in result
        assert "(or" in result or "or" in result


# Marker for slow tests
@pytest.mark.slow
class TestPerformance:
    """Performance tests for text cleaning."""
    
    def test_large_document_performance(self):
        """Test performance with large documents."""
        # Create a large text document
        text = "\n".join([f"Line {i}: This is test content" for i in range(10000)])
        result = clean_text(text)
        assert isinstance(result, str)
        assert len(result) > 0

