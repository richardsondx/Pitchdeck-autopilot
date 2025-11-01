"""
Markdown Builder Module - Generate formatted markdown output from analysis.
"""

import os
import re
from datetime import datetime
from typing import Dict, List
from .ai_analyzer import AnalysisResult


def build_markdown(analysis: AnalysisResult, slide_count: int, ocr_count: int = 0) -> str:
    """
    Build a beautifully formatted markdown document from analysis results.
    
    Args:
        analysis: AnalysisResult object with structured data
        slide_count: Total number of slides processed
        ocr_count: Number of slides processed with OCR
    
    Returns:
        Formatted markdown string
    """
    sections = []
    
    # Header
    sections.append(f"# Company Brief: {analysis.company}")
    sections.append("")
    
    # Metadata
    metadata = []
    metadata.append(f"**Deck Parsed:** {slide_count} slides")
    if ocr_count > 0:
        metadata.append(f"**OCR Used:** {ocr_count} slides")
    metadata.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Simple confidence estimation based on content completeness
    confidence = calculate_confidence(analysis)
    metadata.append(f"**Confidence:** {confidence}%")
    
    sections.append("  \n".join(metadata))
    sections.append("")
    sections.append("---")
    sections.append("")
    
    # Tagline (if present)
    if analysis.tagline:
        sections.append(f"**{analysis.tagline}**")
        sections.append("")
        sections.append("---")
        sections.append("")
    
    # Investment Rubric (if scores available)
    if analysis.investment_scores:
        sections.append("### 🧮 Apple-to-Apple Investment Snapshot")
        sections.append("")
        sections.append("| Pillar | Score | Comment |")
        sections.append("|--------|-------|---------|")
        
        score_map = {
            "founder_market_fit": "Founder-Market Fit",
            "problem_severity": "Problem Severity",
            "solution_quality": "Solution Quality",
            "traction_momentum": "Traction Momentum",
            "market_size": "Market Size & Timing",
            "moat_potential": "Moat Potential",
            "risk_level": "Risk Level"
        }
        
        total_score = 0
        count = 0
        
        for key, label in score_map.items():
            if key in analysis.investment_scores:
                score_data = analysis.investment_scores[key]
                score = score_data.get("score", 0)
                reasoning = score_data.get("reasoning", "")
                emoji = get_score_emoji(score)
                sections.append(f"| {label} | {emoji} {score}/5 | {reasoning} |")
                total_score += score
                count += 1
        
        if count > 0:
            avg_score = total_score / count
            overall_emoji = get_overall_emoji(avg_score)
            sections.append("")
            sections.append(f"**Overall Fit:** {overall_emoji} (Weighted Avg {avg_score:.1f}/5)")
        
        sections.append("")
        sections.append("---")
        sections.append("")
    
    # Main sections with icons
    content_sections = [
        ("🧩 Problem", analysis.problem),
        ("🚀 Solution", analysis.solution),
        ("📈 Traction", analysis.traction),
        ("👥 Team", analysis.team),
        ("🌍 Market", analysis.market),
        ("🧱 Moat", analysis.moat),
        ("⚠️ Risks", analysis.risks),
    ]
    
    for title, content in content_sections:
        if content and content.strip():
            sections.append(f"### {title}")
            sections.append("")
            sections.append(content.strip())
            sections.append("")
    
    # Labeled Sources (with fallback to old Sources)
    if analysis.labeled_sources:
        sections.append("---")
        sections.append("")
        sections.append("### 📚 Sources")
        sections.append("")
        for source in analysis.labeled_sources:
            slides = source.get("slides", "")
            content = source.get("content", "")
            sections.append(f"- {slides} — {content}")
        sections.append("")
    elif analysis.sources:
        # Fallback to old format if labeled sources not available
        sections.append("---")
        sections.append("")
        sections.append("### 📚 Sources")
        sections.append("")
        for source in analysis.sources:
            sections.append(f"- {source}")
        sections.append("")
    
    return "\n".join(sections)


def calculate_confidence(analysis: AnalysisResult) -> int:
    """
    Calculate a confidence score based on how complete the analysis is.
    
    Args:
        analysis: AnalysisResult object
    
    Returns:
        Confidence score from 0-100
    """
    # Check which fields have substantial content
    fields_to_check = [
        analysis.company,
        analysis.problem,
        analysis.solution,
        analysis.traction,
        analysis.team,
        analysis.market,
    ]
    
    filled_count = 0
    for field in fields_to_check:
        if field and len(field.strip()) > 10:  # At least 10 chars
            filled_count += 1
    
    # Base confidence on percentage of fields filled
    base_confidence = (filled_count / len(fields_to_check)) * 100
    
    # Bonus points for having sources
    if analysis.sources and len(analysis.sources) > 0:
        base_confidence = min(100, base_confidence + 10)
    
    return int(base_confidence)


def get_score_emoji(score: int) -> str:
    """
    Get emoji indicator for investment score.
    
    Args:
        score: Score from 0-5
    
    Returns:
        Emoji string (green/yellow/red square)
    """
    if score >= 4:
        return "🟩"
    elif score >= 2:
        return "🟨"
    else:
        return "🟥"


def get_overall_emoji(avg: float) -> str:
    """
    Get overall assessment emoji based on average score.
    
    Args:
        avg: Average score from 0-5
    
    Returns:
        Emoji with label (Strong/Moderate/Weak)
    """
    if avg >= 4.0:
        return "🟩 Strong"
    elif avg >= 3.0:
        return "🟨 Moderate"
    else:
        return "🟥 Weak"


def sanitize_filename(company_name: str) -> str:
    """
    Sanitize company name for use as filename.
    
    Args:
        company_name: Company name from analysis
    
    Returns:
        Safe filename string
    """
    # Remove or replace invalid filename characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '', company_name)
    
    # Replace spaces with underscores
    safe_name = safe_name.replace(' ', '_')
    
    # Limit length
    if len(safe_name) > 50:
        safe_name = safe_name[:50]
    
    # Remove trailing dots and spaces
    safe_name = safe_name.rstrip('. ')
    
    # If name is empty after sanitization, use default
    if not safe_name:
        safe_name = "Company"
    
    return safe_name


def save_markdown(markdown_content: str, company_name: str, output_dir: str = "output") -> str:
    """
    Save markdown content to a file.
    
    Args:
        markdown_content: The markdown text to save
        company_name: Company name for filename
        output_dir: Directory to save output file
    
    Returns:
        Path to the saved file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate filename
    safe_name = sanitize_filename(company_name)
    filename = f"{safe_name}_Brief.md"
    filepath = os.path.join(output_dir, filename)
    
    # Handle duplicate filenames by adding timestamp
    if os.path.exists(filepath):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{safe_name}_Brief_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return filepath


def save_debug_info(raw_text: str, raw_response: str, output_dir: str = "debug") -> None:
    """
    Save debug information for troubleshooting.
    
    Args:
        raw_text: Raw extracted text
        raw_response: Raw API response
        output_dir: Directory for debug files
    """
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Save raw extraction
    extraction_file = os.path.join(output_dir, f"extraction_{timestamp}.txt")
    with open(extraction_file, 'w', encoding='utf-8') as f:
        f.write(raw_text)
    
    # Save raw API response
    if raw_response:
        response_file = os.path.join(output_dir, f"api_response_{timestamp}.txt")
        with open(response_file, 'w', encoding='utf-8') as f:
            f.write(raw_response)

