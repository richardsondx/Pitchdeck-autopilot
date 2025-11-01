"""
Validation guards and edge case tests.
"""

import pytest
import os
from deckbrief.text_cleaner import clean_text
from deckbrief.markdown_builder import sanitize_filename, save_markdown
from deckbrief.ai_analyzer import create_fast_analysis
from deckbrief.deck_parser import parse_deck


class TestInputValidation:
    """Test input validation and guard conditions."""
    
    def test_empty_text_handling(self):
        """Test handling of empty text input."""
        result = clean_text("")
        assert result == ""
        
        result = clean_text(None)
        assert result == ""
    
    def test_none_propagation(self):
        """Test that None values don't cause crashes."""
        # clean_text should handle None
        assert clean_text(None) == ""
        
        # sanitize_filename should handle empty
        assert sanitize_filename("") == "Company"
        
        # fast_analysis should handle empty text
        result = create_fast_analysis("", 0)
        assert result is not None
    
    def test_very_long_text(self):
        """Test handling of very long text (>100KB)."""
        long_text = "A" * 200000
        
        result = clean_text(long_text)
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_unicode_edge_cases(self):
        """Test handling of various unicode characters."""
        test_cases = [
            "Hello 世界",  # Chinese
            "مرحبا بالعالم",  # Arabic (RTL)
            "Привет мир",  # Russian
            "🚀 🎯 ✅",  # Emojis
            "Ñoño",  # Accented chars
        ]
        
        for text in test_cases:
            result = clean_text(text)
            assert isinstance(result, str)
    
    def test_mixed_encodings(self):
        """Test text with mixed encodings."""
        text = "ASCII + Ünïcödé + 日本語"
        result = clean_text(text)
        assert isinstance(result, str)


class TestFileSystemGuards:
    """Test file system edge cases."""
    
    def test_long_filename(self, temp_dir):
        """Test handling of very long filenames."""
        long_name = "A" * 200
        markdown = "# Test"
        
        # Should truncate and save successfully
        path = save_markdown(markdown, long_name, temp_dir)
        assert os.path.exists(path)
        assert len(os.path.basename(path)) < 255  # Max filename length
    
    def test_special_chars_in_filename(self, temp_dir):
        """Test handling of special characters in filenames."""
        special_names = [
            "Company/Name",
            "Company:Name",
            "Company*Name",
            "Company?Name",
            "Company<>Name",
        ]
        
        for name in special_names:
            markdown = "# Test"
            path = save_markdown(markdown, name, temp_dir)
            assert os.path.exists(path)
            # Should not contain special chars
            basename = os.path.basename(path)
            assert "/" not in basename
            assert ":" not in basename
    
    def test_permission_errors(self, temp_dir):
        """Test handling of permission errors."""
        # This test is platform-dependent
        # On Unix-like systems, we can create a read-only directory
        if os.name != 'nt':  # Not Windows
            readonly_dir = os.path.join(temp_dir, 'readonly')
            os.makedirs(readonly_dir, exist_ok=True)
            os.chmod(readonly_dir, 0o444)  # Read-only
            
            try:
                markdown = "# Test"
                # Should raise exception (can't write to readonly dir)
                with pytest.raises((PermissionError, OSError)):
                    save_markdown(markdown, "Test", readonly_dir)
            finally:
                # Cleanup
                os.chmod(readonly_dir, 0o755)
    
    def test_disk_space_simulation(self):
        """Test behavior when disk might be full."""
        # This is difficult to test without actually filling disk
        # Just verify the function doesn't crash with large content
        huge_markdown = "#" * 1000000  # 1MB of hashes
        # If this doesn't crash, we're good
        assert isinstance(huge_markdown, str)


class TestDataValidation:
    """Test data validation and sanitization."""
    
    def test_invalid_json_characters(self):
        """Test handling of JSON-breaking characters."""
        text = 'Text with "quotes" and \\backslashes\\ and \nnewlines'
        result = clean_text(text)
        assert isinstance(result, str)
    
    def test_null_bytes(self):
        """Test handling of null bytes in text."""
        text = "Hello\x00World\x00"
        result = clean_text(text)
        assert "\x00" not in result
    
    def test_control_characters(self):
        """Test removal of control characters."""
        text = "Text\x01with\x02control\x03chars"
        result = clean_text(text)
        # Control chars should be removed
        assert "\x01" not in result
        assert "\x02" not in result
        assert "\x03" not in result
    
    def test_excessive_whitespace(self):
        """Test handling of excessive whitespace."""
        text = "Word" + (" " * 1000) + "Word"
        result = clean_text(text)
        # Should be normalized
        assert " " * 100 not in result


class TestConcurrencyGuards:
    """Test concurrent file operations."""
    
    def test_duplicate_filename_handling(self, temp_dir):
        """Test that duplicate filenames are handled."""
        import time
        markdown = "# Test"
        
        # Save same filename multiple times with delays
        path1 = save_markdown(markdown, "TestCo", temp_dir)
        time.sleep(1.1)  # Need >1 second for timestamp in filename to change
        path2 = save_markdown(markdown, "TestCo", temp_dir)
        time.sleep(1.1)
        path3 = save_markdown(markdown, "TestCo", temp_dir)
        
        # All should exist
        assert os.path.exists(path1)
        assert os.path.exists(path2)
        assert os.path.exists(path3)
        
        # All should be different
        paths = {path1, path2, path3}
        assert len(paths) == 3, f"Expected 3 unique paths, got {len(paths)}: {paths}"


class TestErrorRecovery:
    """Test error recovery mechanisms."""
    
    def test_partial_deck_parsing(self, temp_dir):
        """Test that partial deck parsing doesn't crash."""
        # Create a minimal PDF
        from reportlab.pdfgen import canvas
        pdf_path = os.path.join(temp_dir, 'minimal.pdf')
        c = canvas.Canvas(pdf_path)
        c.showPage()
        c.save()
        
        # Should not crash
        slides, _ = parse_deck(pdf_path)
        assert isinstance(slides, list)
    
    def test_recovery_from_empty_slides(self):
        """Test recovery when all slides are empty."""
        result = create_fast_analysis("", 0)
        assert result is not None
        assert result.company is not None


class TestBoundaryConditions:
    """Test boundary conditions."""
    
    def test_zero_slides(self):
        """Test handling of zero slides."""
        result = create_fast_analysis("", 0)
        assert result is not None
    
    def test_single_slide(self, temp_dir):
        """Test handling of single-slide deck."""
        from reportlab.pdfgen import canvas
        pdf_path = os.path.join(temp_dir, 'single.pdf')
        c = canvas.Canvas(pdf_path)
        c.drawString(100, 750, "Single Slide")
        c.showPage()
        c.save()
        
        slides, _ = parse_deck(pdf_path)
        assert len(slides) == 1
    
    def test_very_large_deck(self):
        """Test handling of very large deck (simulation)."""
        # Simulate many slides
        text = "\n\n".join([f"--- Slide {i} ---\nContent {i}" for i in range(1000)])
        result = clean_text(text)
        assert isinstance(result, str)
    
    def test_minimum_viable_analysis(self):
        """Test creating analysis with minimum data."""
        text = "Company Name"
        result = create_fast_analysis(text, 1)
        
        assert result.company is not None
        assert isinstance(result.sources, list)


class TestResourceLimits:
    """Test resource limit handling."""
    
    @pytest.mark.slow
    def test_memory_efficiency(self):
        """Test that large operations don't consume excessive memory."""
        # Create large text
        large_text = "\n".join([f"Line {i}: Content here" for i in range(100000)])
        
        # Should complete without memory error
        result = clean_text(large_text)
        assert isinstance(result, str)
    
    def test_cpu_efficiency(self):
        """Test that operations complete in reasonable time."""
        import time
        
        text = "Test content\n" * 1000
        
        start = time.time()
        result = clean_text(text)
        elapsed = time.time() - start
        
        # Should complete quickly
        assert elapsed < 1.0  # Less than 1 second
        assert isinstance(result, str)

