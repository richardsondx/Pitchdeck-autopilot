"""
AI Analyzer Module - OpenRouter API integration for deck analysis.
"""

import requests
import json
import time
import os
from typing import Dict, Optional


class AnalysisResult:
    """Container for AI analysis results."""
    
    def __init__(self, data: Dict, raw_response: str = ""):
        self.company = data.get("Company", "Unknown Company")
        self.tagline = data.get("Tagline", "")
        self.problem = data.get("Problem", "")
        self.solution = data.get("Solution", "")
        self.traction = data.get("Traction", "")
        self.team = data.get("Team", "")
        self.market = data.get("Market", "")
        self.moat = data.get("Moat", "")
        self.risks = data.get("Risks", "")
        self.sources = data.get("Sources", [])
        self.labeled_sources = data.get("LabeledSources", [])
        self.investment_scores = data.get("InvestmentScores", {})
        self.raw_response = raw_response
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for markdown generation."""
        return {
            "Company": self.company,
            "Tagline": self.tagline,
            "Problem": self.problem,
            "Solution": self.solution,
            "Traction": self.traction,
            "Team": self.team,
            "Market": self.market,
            "Moat": self.moat,
            "Risks": self.risks,
            "Sources": self.sources,
        }


def analyze_deck(deck_text: str, api_key: str, max_retries: int = 2) -> AnalysisResult:
    """
    Analyze deck content using OpenRouter AI.
    
    Args:
        deck_text: Cleaned text from the deck
        api_key: OpenRouter API key
        max_retries: Number of retry attempts for API failures
    
    Returns:
        AnalysisResult object with structured analysis
    
    Raises:
        ValueError: If API call fails after retries or response is invalid
    """
    if not api_key or api_key == "your_api_key_here":
        raise ValueError(
            "Invalid OpenRouter API key. Please set OPENROUTER_API_KEY in your .env file.\n"
            "Get your key from: https://openrouter.ai/keys"
        )
    
    # Truncate text if too long (keep first ~15000 chars to stay within token limits)
    if len(deck_text) > 15000:
        deck_text = deck_text[:15000] + "\n\n[Content truncated for API limits]"
    
    prompt = create_analysis_prompt(deck_text)
    
    for attempt in range(max_retries + 1):
        try:
            response = call_openrouter(prompt, api_key)
            analysis_data = parse_response(response)
            return AnalysisResult(analysis_data, response)
        
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise ValueError("OpenRouter API request timed out after multiple retries")
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
            raise ValueError(f"OpenRouter API request failed: {str(e)}")
        
        except json.JSONDecodeError as e:
            if attempt < max_retries:
                time.sleep(2 ** attempt)
                continue
            # If we still can't parse JSON, try to extract what we can
            return create_fallback_analysis(response if 'response' in locals() else "")


def create_analysis_prompt(deck_text: str) -> str:
    """Create the prompt for AI analysis."""
    
    prompt = """You are an expert investment analyst reviewing a startup pitch deck.

Analyze the following deck content and extract key information into a structured JSON format.

**IMPORTANT**: Respond ONLY with valid JSON matching this exact schema:

{
  "Company": "Company name",
  "Tagline": "One-line description",
  "Problem": "What problem they're solving",
  "Solution": "Their product/service solution",
  "Traction": "Growth metrics, revenue, customers, or traction indicators",
  "Team": "Key team members and their backgrounds",
  "Market": "Market size, TAM/SAM/SOM, or market opportunity",
  "Moat": "Competitive advantages or defensibility",
  "Risks": "Key risks or challenges identified",
  "LabeledSources": [
    {"slides": "Slide 1-2", "content": "Company overview and tagline"},
    {"slides": "Slide 3", "content": "Problem statement"},
    {"slides": "Slide 4-5", "content": "Solution and product demo"}
  ],
  "InvestmentScores": {
    "founder_market_fit": {"score": 5, "reasoning": "Brief explanation"},
    "problem_severity": {"score": 4, "reasoning": "Brief explanation"},
    "solution_quality": {"score": 4, "reasoning": "Brief explanation"},
    "traction_momentum": {"score": 3, "reasoning": "Brief explanation"},
    "market_size": {"score": 5, "reasoning": "Brief explanation"},
    "moat_potential": {"score": 3, "reasoning": "Brief explanation"},
    "risk_level": {"score": 3, "reasoning": "Brief explanation"}
  }
}

Guidelines:
- If information is not found in the deck, use empty string ""
- Be concise but informative (2-3 sentences per field)
- Focus on facts from the deck, not speculation

LabeledSources Guidelines:
- Group related slides together (e.g., "Slide 1-2", "Slide 5-7")
- Provide a brief description of what content each slide/group contributed
- Examples: "Company overview and tagline", "Problem statement", "Market size analysis"

InvestmentScores Guidelines (0-5 scale):
- founder_market_fit: Does the founder clearly belong to this market? (5=strong domain expertise, 1=no clear connection)
- problem_severity: Is this a "hair-on-fire" problem or a vitamin? (5=critical pain point, 1=nice-to-have)
- solution_quality: Is it truly differentiated or incremental? (5=novel approach, 1=commodity)
- traction_momentum: Evidence of pull (users, growth, revenue)? (5=strong metrics, 1=pre-launch)
- market_size: How large and ripe is the opportunity now? (5=huge addressable market, 1=niche)
- moat_potential: Network/data/distribution advantages? (5=strong defensibility, 1=easily replicable)
- risk_level: Funding, competition, regulatory, execution risks? (5=low risk, 1=high risk)
- Keep reasoning to 1 sentence per score

Deck Content:
<<<START_DECK>>>
""" + deck_text + """
<<<END_DECK>>>

Respond with ONLY the JSON object, no other text."""

    return prompt


def call_openrouter(prompt: str, api_key: str, timeout: int = 60) -> str:
    """
    Make API call to OpenRouter.
    
    Args:
        prompt: The analysis prompt
        api_key: OpenRouter API key
        timeout: Request timeout in seconds
    
    Returns:
        Raw response text from the API
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/pitchdeck-autopilot",
        "X-Title": "PitchDeck Autopilot"
    }
    
    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,  # Lower temperature for more consistent structured output
        "max_tokens": 2000,
    }
    
    response = requests.post(url, headers=headers, json=data, timeout=timeout)
    response.raise_for_status()
    
    result = response.json()
    
    if "choices" not in result or len(result["choices"]) == 0:
        raise ValueError("Invalid API response: no choices returned")
    
    return result["choices"][0]["message"]["content"]


def parse_response(response_text: str) -> Dict:
    """
    Parse the AI response into structured data.
    
    Args:
        response_text: Raw response from API
    
    Returns:
        Dictionary with analysis data
    """
    # Try to extract JSON from the response
    # Sometimes the model adds markdown code blocks
    response_text = response_text.strip()
    
    # Remove markdown code blocks if present
    if response_text.startswith("```"):
        # Find the first { and last }
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start != -1 and end > start:
            response_text = response_text[start:end]
    
    try:
        data = json.loads(response_text)
        
        # Validate that we have the expected structure
        expected_keys = ["Company", "Tagline", "Problem", "Solution", "Traction", 
                        "Team", "Market", "Moat", "Risks", "Sources"]
        
        # Fill in missing keys with empty strings
        for key in expected_keys:
            if key not in data:
                data[key] = "" if key != "Sources" else []
        
        # Handle new optional fields (for backward compatibility)
        if "LabeledSources" not in data:
            data["LabeledSources"] = []
        
        if "InvestmentScores" not in data:
            data["InvestmentScores"] = {}
        
        return data
    
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Failed to parse AI response as JSON: {str(e)}", 
            response_text, 
            e.pos
        )


def create_fallback_analysis(response_text: str) -> AnalysisResult:
    """
    Create a basic analysis when JSON parsing fails.
    
    Args:
        response_text: Raw response text
    
    Returns:
        AnalysisResult with whatever we could extract
    """
    return AnalysisResult({
        "Company": "Unknown Company",
        "Tagline": "Analysis parsing failed",
        "Problem": response_text[:200] if response_text else "Unable to analyze deck",
        "Solution": "",
        "Traction": "",
        "Team": "",
        "Market": "",
        "Moat": "",
        "Risks": "AI analysis could not be parsed properly",
        "Sources": [],
    }, response_text)


def create_fast_analysis(deck_text: str, slide_count: int) -> AnalysisResult:
    """
    Create a basic analysis without AI (for --fast mode).
    
    Args:
        deck_text: Cleaned text from the deck
        slide_count: Number of slides extracted
    
    Returns:
        AnalysisResult with basic extraction info
    """
    # Try to extract company name from first few lines
    lines = deck_text.split('\n')
    company_name = "Unknown Company"
    
    for line in lines[:10]:
        line = line.strip()
        if line and len(line) < 50 and len(line) > 3:
            # Heuristic: first substantial line might be company name
            if not line.startswith('---'):
                company_name = line
                break
    
    return AnalysisResult({
        "Company": company_name,
        "Tagline": "Fast extraction mode - AI analysis skipped",
        "Problem": "Enable AI mode for detailed analysis",
        "Solution": f"This deck contains {slide_count} slides with {len(deck_text)} characters of content.",
        "Traction": "Not analyzed in fast mode",
        "Team": "Not analyzed in fast mode",
        "Market": "Not analyzed in fast mode",
        "Moat": "Not analyzed in fast mode",
        "Risks": "Not analyzed in fast mode",
        "Sources": ["Direct extraction"],
    })

