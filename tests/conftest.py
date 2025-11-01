"""
Shared fixtures for test suite.
"""

import pytest
import os
import json
import tempfile
import shutil
from pathlib import Path
from click.testing import CliRunner
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pptx import Presentation
from pptx.util import Inches


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    tmp = tempfile.mkdtemp()
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


@pytest.fixture
def output_dir(temp_dir):
    """Create an output directory for test artifacts."""
    output = os.path.join(temp_dir, 'output')
    os.makedirs(output, exist_ok=True)
    return output


@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables."""
    monkeypatch.setenv('OPENROUTER_API_KEY', 'test-api-key-12345')
    return {
        'OPENROUTER_API_KEY': 'test-api-key-12345'
    }


@pytest.fixture
def sample_pdf_path(temp_dir):
    """Create a sample PDF file for testing."""
    pdf_path = os.path.join(temp_dir, 'test_deck.pdf')
    
    # Create a simple PDF with text
    c = canvas.Canvas(pdf_path, pagesize=letter)
    
    # Page 1 - Title
    c.drawString(100, 750, "TestCo Robotics")
    c.drawString(100, 700, "AI-Native Robotics Platform")
    c.showPage()
    
    # Page 2 - Problem
    c.drawString(100, 750, "The Problem")
    c.drawString(100, 700, "Industrial robots are expensive and data-hungry.")
    c.drawString(100, 680, "Training requires months of real-world data.")
    c.showPage()
    
    # Page 3 - Solution
    c.drawString(100, 750, "Our Solution")
    c.drawString(100, 700, "Synthetic data generation for robot training.")
    c.drawString(100, 680, "10x faster deployment than traditional methods.")
    c.showPage()
    
    # Page 4 - Traction
    c.drawString(100, 750, "Traction")
    c.drawString(100, 700, "2 pilot customers")
    c.drawString(100, 680, "$250K committed ARR")
    c.showPage()
    
    c.save()
    return pdf_path


@pytest.fixture
def sample_pptx_path(temp_dir):
    """Create a sample PPTX file for testing."""
    pptx_path = os.path.join(temp_dir, 'test_deck.pptx')
    
    prs = Presentation()
    
    # Slide 1 - Title
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    title = slide.shapes.title
    title.text = "TestCo Robotics"
    subtitle = slide.placeholders[1]
    subtitle.text = "AI-Native Robotics Platform"
    
    # Slide 2 - Content
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "The Problem"
    content = slide.placeholders[1]
    content.text = "Industrial robots are expensive\nTraining requires real-world data"
    
    # Slide 3 - Content
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    title = slide.shapes.title
    title.text = "Our Solution"
    content = slide.placeholders[1]
    content.text = "Synthetic data generation\n10x faster deployment"
    
    prs.save(pptx_path)
    return pptx_path


@pytest.fixture
def empty_pdf_path(temp_dir):
    """Create an empty PDF file for testing."""
    pdf_path = os.path.join(temp_dir, 'empty.pdf')
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.showPage()
    c.save()
    return pdf_path


@pytest.fixture
def corrupted_file_path(temp_dir):
    """Create a corrupted file for error testing."""
    file_path = os.path.join(temp_dir, 'corrupted.pdf')
    with open(file_path, 'w') as f:
        f.write("This is not a valid PDF file")
    return file_path


@pytest.fixture
def openrouter_responses():
    """Load mocked OpenRouter API responses."""
    mocks_path = Path(__file__).parent / 'mocks' / 'openrouter_responses.json'
    with open(mocks_path, 'r') as f:
        return json.load(f)


@pytest.fixture
def cli_runner():
    """Click CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_deck_text():
    """Sample cleaned deck text for testing."""
    return """--- Slide 1 ---
TestCo Robotics
AI-Native Robotics Platform

--- Slide 2 ---
The Problem
Industrial robots are expensive and data-hungry
Training requires months of real-world data collection

--- Slide 3 ---
Our Solution
Synthetic data generation for robot training
10x faster deployment than traditional methods
Proprietary simulation environment

--- Slide 4 ---
Traction
2 pilot customers in automotive manufacturing
$250K in committed ARR for 2025
15,000 hours of simulation data generated

--- Slide 5 ---
Team
Founded by ex-DeepMind engineers
PhDs from MIT and Stanford
Combined 20 years experience in ML and robotics"""


@pytest.fixture
def sample_analysis_data():
    """Sample analysis result data for testing."""
    return {
        "Company": "TestCo Robotics",
        "Tagline": "AI-native robotics platform",
        "Problem": "Industrial robots are expensive and data-hungry",
        "Solution": "Synthetic data generation for robot training",
        "Traction": "2 pilot customers, $250K ARR",
        "Team": "Ex-DeepMind engineers with PhDs",
        "Market": "$8.3B market growing 19% CAGR",
        "Moat": "Proprietary simulation dataset",
        "Risks": "Hardware costs and compute dependency",
        "Sources": ["Slide 3", "Slide 12", "Slide 28"]
    }


# Cleanup old test todos (the duplicate ones from previous plan)
@pytest.fixture(scope="session", autouse=True)
def cleanup_duplicate_todos():
    """Remove duplicate todos from previous plan iteration."""
    # This is handled separately, not in fixtures
    pass


