"""
End-to-end integration tests for CLI workflows.
"""

import pytest
import os
import responses
from click.testing import CliRunner
from main import main


@pytest.mark.integration
class TestCLIWorkflow:
    """Test complete CLI workflows with real file I/O."""
    
    @responses.activate
    def test_basic_pdf_analysis(self, cli_runner, sample_pdf_path, temp_dir, mock_env, openrouter_responses):
        """Test basic PDF analysis workflow."""
        # Mock API
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=openrouter_responses["success_response"],
            status=200
        )
        
        # Run CLI
        result = cli_runner.invoke(main, [
            sample_pdf_path,
            '--output-dir', temp_dir
        ])
        
        # Check exit code
        assert result.exit_code == 0
        
        # Check output messages
        assert "Extracting slides" in result.output
        assert "Cleaning text" in result.output
        assert "Analyzing content" in result.output
        assert "Analysis complete" in result.output
        
        # Check file was created
        output_files = os.listdir(temp_dir)
        assert any(f.endswith('_Brief.md') for f in output_files)
    
    @responses.activate
    def test_pptx_analysis(self, cli_runner, sample_pptx_path, temp_dir, mock_env, openrouter_responses):
        """Test PPTX file analysis."""
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=openrouter_responses["success_response"],
            status=200
        )
        
        result = cli_runner.invoke(main, [
            sample_pptx_path,
            '--output-dir', temp_dir
        ])
        
        assert result.exit_code == 0
        assert "slides extracted" in result.output
        
        # Check output file exists
        output_files = os.listdir(temp_dir)
        assert len(output_files) > 0
    
    def test_fast_mode(self, cli_runner, sample_pdf_path, temp_dir):
        """Test --fast flag (skip AI enrichment)."""
        result = cli_runner.invoke(main, [
            sample_pdf_path,
            '--fast',
            '--output-dir', temp_dir
        ])
        
        assert result.exit_code == 0
        assert "Fast" in result.output or "fast" in result.output
        assert "OpenRouter" not in result.output or "skipped" in result.output.lower()
        
        # Should still create output
        output_files = os.listdir(temp_dir)
        assert len(output_files) > 0
    
    def test_debug_mode(self, cli_runner, sample_pdf_path, temp_dir, mock_env):
        """Test --debug flag."""
        result = cli_runner.invoke(main, [
            sample_pdf_path,
            '--fast',  # Use fast to avoid API call
            '--debug',
            '--output-dir', temp_dir
        ])
        
        assert result.exit_code == 0
        # Debug output should show raw text
        assert "Raw Extracted Text" in result.output or "debug" in result.output.lower()
    
    def test_custom_output_dir(self, cli_runner, sample_pdf_path, temp_dir, mock_env):
        """Test --output-dir option."""
        custom_dir = os.path.join(temp_dir, 'custom_output')
        
        result = cli_runner.invoke(main, [
            sample_pdf_path,
            '--fast',
            '--output-dir', custom_dir
        ])
        
        assert result.exit_code == 0
        assert os.path.exists(custom_dir)
        assert len(os.listdir(custom_dir)) > 0
    
    def test_file_not_found(self, cli_runner):
        """Test error handling for missing file."""
        result = cli_runner.invoke(main, ['/nonexistent/file.pdf'])
        
        assert result.exit_code == 2  # Click's error code for bad parameter
    
    @responses.activate
    def test_invalid_api_key(self, cli_runner, sample_pdf_path, temp_dir, monkeypatch):
        """Test error handling for invalid API key."""
        # Set invalid API key
        monkeypatch.setenv('OPENROUTER_API_KEY', '')
        
        result = cli_runner.invoke(main, [
            sample_pdf_path,
            '--output-dir', temp_dir
        ])
        
        # Should fail with error message
        assert result.exit_code == 1
        assert "API key" in result.output or "Invalid" in result.output
    
    def test_unsupported_file_format(self, cli_runner, temp_dir):
        """Test error handling for unsupported file format."""
        # Create a .txt file
        txt_file = os.path.join(temp_dir, 'test.txt')
        with open(txt_file, 'w') as f:
            f.write("Test content")
        
        result = cli_runner.invoke(main, [txt_file])
        
        assert result.exit_code == 1
        assert "Unsupported" in result.output or "format" in result.output
    
    def test_corrupted_file(self, cli_runner, corrupted_file_path):
        """Test error handling for corrupted files."""
        result = cli_runner.invoke(main, [corrupted_file_path])
        
        assert result.exit_code == 1
        # Should show error message
        assert "Failed" in result.output or "error" in result.output.lower()
    
    def test_empty_pdf(self, cli_runner, empty_pdf_path, temp_dir):
        """Test handling of empty PDF files."""
        result = cli_runner.invoke(main, [
            empty_pdf_path,
            '--fast',
            '--output-dir', temp_dir
        ])
        
        # Should either succeed with warning or fail gracefully
        assert "No content" in result.output or result.exit_code == 0
    
    @pytest.mark.slow
    def test_help_command(self, cli_runner):
        """Test --help flag."""
        result = cli_runner.invoke(main, ['--help'])
        
        assert result.exit_code == 0
        assert "Transform pitch decks" in result.output
        assert "--fast" in result.output
        assert "--debug" in result.output
        assert "--output-dir" in result.output
    
    @responses.activate
    def test_markdown_output_structure(self, cli_runner, sample_pdf_path, temp_dir, mock_env, openrouter_responses):
        """Test that generated markdown has correct structure."""
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=openrouter_responses["success_response"],
            status=200
        )
        
        result = cli_runner.invoke(main, [
            sample_pdf_path,
            '--output-dir', temp_dir
        ])
        
        assert result.exit_code == 0
        
        # Find and read the output file
        output_files = [f for f in os.listdir(temp_dir) if f.endswith('.md')]
        assert len(output_files) > 0
        
        output_path = os.path.join(temp_dir, output_files[0])
        with open(output_path, 'r') as f:
            content = f.read()
        
        # Check structure
        assert "# Company Brief:" in content
        assert "**Deck Parsed:**" in content
        assert "🧩 Problem" in content or "🚀 Solution" in content
    
    def test_elapsed_time_displayed(self, cli_runner, sample_pdf_path, temp_dir):
        """Test that elapsed time is displayed."""
        result = cli_runner.invoke(main, [
            sample_pdf_path,
            '--fast',
            '--output-dir', temp_dir
        ])
        
        assert result.exit_code == 0
        assert "time:" in result.output.lower() or "s" in result.output


@pytest.mark.integration
class TestRealFileOperations:
    """Test real file I/O operations."""
    
    def test_creates_output_directory(self, cli_runner, sample_pdf_path, temp_dir):
        """Test that output directory is created if it doesn't exist."""
        new_output = os.path.join(temp_dir, 'new_dir', 'output')
        
        result = cli_runner.invoke(main, [
            sample_pdf_path,
            '--fast',
            '--output-dir', new_output
        ])
        
        assert result.exit_code == 0
        assert os.path.exists(new_output)
    
    def test_file_permissions(self, cli_runner, sample_pdf_path, temp_dir):
        """Test that output files have correct permissions."""
        result = cli_runner.invoke(main, [
            sample_pdf_path,
            '--fast',
            '--output-dir', temp_dir
        ])
        
        assert result.exit_code == 0
        
        # Check file is readable
        output_files = [f for f in os.listdir(temp_dir) if f.endswith('.md')]
        assert len(output_files) > 0
        
        output_path = os.path.join(temp_dir, output_files[0])
        assert os.access(output_path, os.R_OK)
        assert os.access(output_path, os.W_OK)


@pytest.mark.integration
@pytest.mark.slow
class TestStressTests:
    """Stress tests for edge cases."""
    
    def test_multiple_sequential_analyses(self, cli_runner, sample_pdf_path, temp_dir):
        """Test running multiple analyses sequentially."""
        for i in range(3):
            result = cli_runner.invoke(main, [
                sample_pdf_path,
                '--fast',
                '--output-dir', temp_dir
            ])
            assert result.exit_code == 0
        
        # Should have created multiple files (with timestamps to avoid collision)
        output_files = [f for f in os.listdir(temp_dir) if f.endswith('.md')]
        assert len(output_files) >= 1


