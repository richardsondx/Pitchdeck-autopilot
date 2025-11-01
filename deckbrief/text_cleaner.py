"""
Text Cleaner Module - Normalize and clean extracted deck content.
"""

import re
from typing import List


def clean_text(text: str) -> str:
    """
    Clean and normalize extracted text from a deck.
    
    Args:
        text: Raw extracted text
    
    Returns:
        Cleaned and normalized text
    """
    if not text:
        return ""
    
    # Remove common headers/footers patterns
    text = remove_headers_footers(text)
    
    # Fix fragmented lines
    text = merge_fragmented_lines(text)
    
    # Normalize whitespace
    text = normalize_whitespace(text)
    
    # Remove excessive special characters
    text = clean_special_characters(text)
    
    return text.strip()


def remove_headers_footers(text: str) -> str:
    """Remove common header and footer patterns."""
    
    # Common patterns to remove
    patterns = [
        r'(?i)^confidential.*$',
        r'(?i)^proprietary.*$',
        r'(?i)^internal use only.*$',
        r'(?i)^draft.*$',
        r'^\d+\s*$',  # Standalone page numbers
        r'^Page \d+ of \d+$',
        r'^\d+/\d+$',  # Page numbers like "1/20"
        r'^©.*$',  # Copyright lines
        r'^Company confidential.*$',
    ]
    
    lines = text.split('\n')
    cleaned_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        
        # Check if line matches any removal pattern
        should_remove = False
        for pattern in patterns:
            if re.match(pattern, line_stripped, re.IGNORECASE):
                should_remove = True
                break
        
        if not should_remove:
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)


def merge_fragmented_lines(text: str) -> str:
    """
    Merge lines that are part of the same sentence but split across lines.
    Preserves intentional line breaks (like bullet points).
    """
    lines = text.split('\n')
    merged_lines = []
    i = 0
    
    while i < len(lines):
        current_line = lines[i].strip()
        
        # If empty line, keep it (paragraph break)
        if not current_line:
            merged_lines.append('')
            i += 1
            continue
        
        # If line starts with bullet/number, don't merge with previous
        if re.match(r'^[\•\-\*\d+\.]\s', current_line):
            merged_lines.append(current_line)
            i += 1
            continue
        
        # If line ends with sentence-ending punctuation, don't merge
        if re.search(r'[.!?:]$', current_line):
            merged_lines.append(current_line)
            i += 1
            continue
        
        # Check if next line looks like a continuation
        if i + 1 < len(lines):
            next_line = lines[i + 1].strip()
            
            # If next line starts with lowercase or is short, might be continuation
            if next_line and next_line[0].islower() and len(current_line) < 80:
                merged_lines.append(current_line + ' ' + next_line)
                i += 2
                continue
        
        merged_lines.append(current_line)
        i += 1
    
    return '\n'.join(merged_lines)


def normalize_whitespace(text: str) -> str:
    """Normalize excessive whitespace while preserving structure."""
    
    # Replace multiple spaces with single space
    text = re.sub(r' +', ' ', text)
    
    # Replace multiple newlines with max 2 (paragraph breaks)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove spaces at start/end of lines
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    
    return text


def clean_special_characters(text: str) -> str:
    """Remove or normalize problematic special characters."""
    
    # Remove null bytes and other control characters (except newlines/tabs)
    text = re.sub(r'[\x00-\x08\x0B-\x0C\x0E-\x1F\x7F]', '', text)
    
    # Normalize unicode quotes and dashes
    replacements = {
        '"': '"',
        '"': '"',
        ''': "'",
        ''': "'",
        '—': '-',
        '–': '-',
        '…': '...',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    # Remove excessive special character sequences
    text = re.sub(r'[^\w\s\n.,!?;:()\[\]{}\-\'\"$%&@#/\\+=<>]{3,}', '', text)
    
    return text


def extract_key_sections(text: str) -> dict:
    """
    Attempt to identify and extract key sections from the deck.
    This is a best-effort extraction that may not work for all decks.
    
    Returns:
        Dictionary with section names as keys and content as values
    """
    sections = {}
    
    # Common section headers in pitch decks
    section_patterns = {
        'problem': r'(?i)(the\s+)?problem|pain\s+point|challenge',
        'solution': r'(?i)(our\s+)?solution|product|platform|service',
        'traction': r'(?i)traction|growth|metrics|revenue|customers',
        'market': r'(?i)market\s+(size|opportunity)|tam|addressable\s+market',
        'team': r'(?i)(our\s+)?team|founders|leadership|management',
        'competition': r'(?i)competi(tion|tors)|landscape|alternatives',
        'business_model': r'(?i)business\s+model|revenue\s+model|monetization',
        'ask': r'(?i)(the\s+)?ask|raising|funding|investment',
    }
    
    lines = text.split('\n')
    current_section = None
    current_content = []
    
    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue
        
        # Check if line is a section header
        matched_section = None
        for section_name, pattern in section_patterns.items():
            if re.match(pattern, line_stripped) and len(line_stripped) < 100:
                matched_section = section_name
                break
        
        if matched_section:
            # Save previous section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            
            # Start new section
            current_section = matched_section
            current_content = []
        elif current_section:
            current_content.append(line_stripped)
    
    # Save last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections

