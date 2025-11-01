"""
API contract tests for ai_analyzer module with mocked HTTP responses.
"""

import pytest
import responses
import json
from requests.exceptions import Timeout, ConnectionError
from deckbrief.ai_analyzer import (
    analyze_deck,
    create_analysis_prompt,
    call_openrouter,
    parse_response,
    create_fallback_analysis,
    create_fast_analysis,
    AnalysisResult,
)


@pytest.mark.api
class TestAnalyzeDeck:
    """Test the main analyze_deck function with mocked API."""
    
    @responses.activate
    def test_successful_analysis(self, sample_deck_text, openrouter_responses):
        """Test successful API call and analysis."""
        # Mock successful API response
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=openrouter_responses["success_response"],
            status=200
        )
        
        result = analyze_deck(sample_deck_text, "test-api-key")
        
        assert isinstance(result, AnalysisResult)
        assert result.company == "TestCo Robotics"
        assert result.tagline == "AI-native robotics platform"
        assert result.problem == "Industrial robots are expensive and data-hungry"
        assert len(result.sources) > 0
    
    @responses.activate
    def test_api_request_structure(self, sample_deck_text):
        """Verify exact HTTP request structure sent to OpenRouter."""
        # Mock response
        mock_response = {
            "choices": [{"message": {"content": '{"Company": "Test", "Tagline": "", "Problem": "", "Solution": "", "Traction": "", "Team": "", "Market": "", "Moat": "", "Risks": "", "Sources": []}'}}]
        }
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=mock_response,
            status=200
        )
        
        analyze_deck(sample_deck_text, "test-api-key")
        
        # Verify request was made
        assert len(responses.calls) == 1
        request = responses.calls[0].request
        
        # Check headers
        assert request.headers["Authorization"] == "Bearer test-api-key"
        assert request.headers["Content-Type"] == "application/json"
        
        # Check payload
        body = json.loads(request.body)
        assert body["model"] == "anthropic/claude-3.5-sonnet"
        assert "messages" in body
        assert body["messages"][0]["role"] == "user"
        assert "temperature" in body
        assert body["temperature"] == 0.3
    
    def test_invalid_api_key(self, sample_deck_text):
        """Test error handling with invalid API key."""
        with pytest.raises(ValueError, match="Invalid OpenRouter API key"):
            analyze_deck(sample_deck_text, "")
        
        with pytest.raises(ValueError, match="Invalid OpenRouter API key"):
            analyze_deck(sample_deck_text, "your_api_key_here")
    
    @responses.activate
    def test_retry_on_timeout(self, sample_deck_text):
        """Test retry logic with timeouts (should fire 3 attempts total)."""
        # First two calls timeout, third succeeds
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            body=Timeout()
        )
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            body=Timeout()
        )
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json={
                "choices": [{
                    "message": {
                        "content": '{"Company": "Test", "Tagline": "", "Problem": "", "Solution": "", "Traction": "", "Team": "", "Market": "", "Moat": "", "Risks": "", "Sources": []}'
                    }
                }]
            },
            status=200
        )
        
        result = analyze_deck(sample_deck_text, "test-api-key", max_retries=2)
        
        # Should have made 3 attempts (1 initial + 2 retries)
        assert len(responses.calls) == 3
        assert isinstance(result, AnalysisResult)
    
    @responses.activate
    def test_all_retries_fail(self, sample_deck_text):
        """Test when all retry attempts fail."""
        # All calls timeout
        for _ in range(3):
            responses.add(
                responses.POST,
                "https://openrouter.ai/api/v1/chat/completions",
                body=Timeout()
            )
        
        with pytest.raises(ValueError, match="timed out"):
            analyze_deck(sample_deck_text, "test-api-key", max_retries=2)
        
        assert len(responses.calls) == 3
    
    @responses.activate
    def test_api_error_401(self, sample_deck_text, openrouter_responses):
        """Test API error handling (401 Unauthorized)."""
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=openrouter_responses["error_401"],
            status=401
        )
        
        with pytest.raises(ValueError, match="API request failed"):
            analyze_deck(sample_deck_text, "test-api-key", max_retries=0)
    
    @responses.activate
    def test_api_error_429(self, sample_deck_text, openrouter_responses):
        """Test API error handling (429 Rate Limit)."""
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=openrouter_responses["error_429"],
            status=429
        )
        
        with pytest.raises(ValueError):
            analyze_deck(sample_deck_text, "test-api-key", max_retries=0)
    
    @responses.activate
    def test_api_error_500(self, sample_deck_text, openrouter_responses):
        """Test API error handling (500 Internal Server Error)."""
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=openrouter_responses["error_500"],
            status=500
        )
        
        with pytest.raises(ValueError):
            analyze_deck(sample_deck_text, "test-api-key", max_retries=0)
    
    @responses.activate
    def test_malformed_json_fallback(self, sample_deck_text, openrouter_responses):
        """Test fallback when API returns non-JSON response."""
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=openrouter_responses["malformed_json_response"],
            status=200
        )
        
        result = analyze_deck(sample_deck_text, "test-api-key", max_retries=0)
        
        # Should return fallback analysis
        assert isinstance(result, AnalysisResult)
        assert "analysis" in result.problem.lower() or "unable" in result.problem.lower()
    
    @responses.activate
    def test_markdown_wrapped_json(self, sample_deck_text, openrouter_responses):
        """Test parsing JSON wrapped in markdown code blocks."""
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=openrouter_responses["markdown_wrapped_response"],
            status=200
        )
        
        result = analyze_deck(sample_deck_text, "test-api-key")
        
        # Should successfully parse despite markdown wrapping
        assert isinstance(result, AnalysisResult)
        assert result.company == "TestCo"
    
    def test_text_truncation(self):
        """Test that very long text is truncated before API call."""
        # Create very long text
        long_text = "A" * 20000
        
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                "https://openrouter.ai/api/v1/chat/completions",
                json={"choices": [{"message": {"content": '{"Company": "Test", "Tagline": "", "Problem": "", "Solution": "", "Traction": "", "Team": "", "Market": "", "Moat": "", "Risks": "", "Sources": []}'}}]},
                status=200
            )
            
            analyze_deck(long_text, "test-api-key")
            
            # Check that sent text was truncated
            request_body = json.loads(rsps.calls[0].request.body)
            prompt = request_body["messages"][0]["content"]
            assert "truncated" in prompt.lower() or len(prompt) < 20000


class TestCreateAnalysisPrompt:
    """Test prompt construction."""
    
    def test_prompt_contains_deck_text(self, sample_deck_text):
        """Test that prompt includes the deck text."""
        prompt = create_analysis_prompt(sample_deck_text)
        
        assert sample_deck_text in prompt
        assert "<<<START_DECK>>>" in prompt
        assert "<<<END_DECK>>>" in prompt
    
    def test_prompt_requests_json(self, sample_deck_text):
        """Test that prompt requests JSON format."""
        prompt = create_analysis_prompt(sample_deck_text)
        
        assert "JSON" in prompt
        assert "Company" in prompt
        assert "Problem" in prompt
        assert "Solution" in prompt
    
    def test_prompt_includes_guidelines(self, sample_deck_text):
        """Test that prompt includes analysis guidelines."""
        prompt = create_analysis_prompt(sample_deck_text)
        
        assert "analyst" in prompt.lower()
        assert "investment" in prompt.lower() or "pitch" in prompt.lower()


class TestCallOpenRouter:
    """Test direct API calling function."""
    
    @responses.activate
    def test_successful_api_call(self):
        """Test successful API call."""
        mock_response = {
            "choices": [{"message": {"content": "Test response"}}]
        }
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json=mock_response,
            status=200
        )
        
        result = call_openrouter("Test prompt", "test-api-key")
        
        assert result == "Test response"
    
    @responses.activate
    def test_api_timeout(self):
        """Test API timeout handling."""
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            body=Timeout()
        )
        
        with pytest.raises(Timeout):
            call_openrouter("Test prompt", "test-api-key", timeout=1)
    
    @responses.activate
    def test_empty_choices(self):
        """Test handling of empty choices in response."""
        responses.add(
            responses.POST,
            "https://openrouter.ai/api/v1/chat/completions",
            json={"choices": []},
            status=200
        )
        
        with pytest.raises(ValueError, match="no choices"):
            call_openrouter("Test prompt", "test-api-key")


class TestParseResponse:
    """Test response parsing."""
    
    def test_parse_valid_json(self):
        """Test parsing valid JSON response."""
        response = '{"Company": "TestCo", "Tagline": "Test", "Problem": "Test problem", "Solution": "Test solution", "Traction": "", "Team": "", "Market": "", "Moat": "", "Risks": "", "Sources": []}'
        
        result = parse_response(response)
        
        assert result["Company"] == "TestCo"
        assert result["Tagline"] == "Test"
        assert "Sources" in result
    
    def test_parse_markdown_wrapped_json(self):
        """Test parsing JSON in markdown code blocks."""
        response = '```json\n{"Company": "TestCo", "Tagline": "", "Problem": "", "Solution": "", "Traction": "", "Team": "", "Market": "", "Moat": "", "Risks": "", "Sources": []}\n```'
        
        result = parse_response(response)
        
        assert result["Company"] == "TestCo"
    
    def test_parse_missing_fields(self):
        """Test that missing fields are filled with defaults."""
        response = '{"Company": "TestCo"}'
        
        result = parse_response(response)
        
        # Should have all expected keys
        assert "Company" in result
        assert "Tagline" in result
        assert "Problem" in result
        assert "Sources" in result
        
        # Missing fields should be empty
        assert result["Tagline"] == ""
        assert result["Sources"] == []
    
    def test_parse_invalid_json(self):
        """Test error handling for invalid JSON."""
        response = "This is not JSON at all"
        
        with pytest.raises(json.JSONDecodeError):
            parse_response(response)


class TestCreateFallbackAnalysis:
    """Test fallback analysis creation."""
    
    def test_fallback_with_response(self):
        """Test fallback analysis with response text."""
        response = "Some analysis text that failed to parse"
        
        result = create_fallback_analysis(response)
        
        assert isinstance(result, AnalysisResult)
        assert result.company == "Unknown Company"
        assert "analysis" in result.tagline.lower() or "failed" in result.tagline.lower()
    
    def test_fallback_empty_response(self):
        """Test fallback analysis with empty response."""
        result = create_fallback_analysis("")
        
        assert isinstance(result, AnalysisResult)
        assert result.company == "Unknown Company"


class TestCreateFastAnalysis:
    """Test fast mode analysis (no AI)."""
    
    def test_fast_analysis_basic(self, sample_deck_text):
        """Test basic fast analysis."""
        result = create_fast_analysis(sample_deck_text, slide_count=10)
        
        assert isinstance(result, AnalysisResult)
        assert "Fast" in result.tagline or "fast" in result.tagline
        assert "10 slides" in result.solution
    
    def test_fast_analysis_extracts_name(self):
        """Test that fast analysis attempts to extract company name."""
        text = "--- Slide 1 ---\nAcme Corp\nAI Platform"
        
        result = create_fast_analysis(text, slide_count=5)
        
        # Should attempt to extract company name from first lines
        assert result.company != "Unknown Company" or "Acme" in text


class TestAnalysisResult:
    """Test AnalysisResult class."""
    
    def test_create_analysis_result(self, sample_analysis_data):
        """Test creating AnalysisResult from data."""
        result = AnalysisResult(sample_analysis_data)
        
        assert result.company == sample_analysis_data["Company"]
        assert result.tagline == sample_analysis_data["Tagline"]
        assert result.problem == sample_analysis_data["Problem"]
        assert result.sources == sample_analysis_data["Sources"]
    
    def test_to_dict(self, sample_analysis_data):
        """Test converting AnalysisResult to dictionary."""
        result = AnalysisResult(sample_analysis_data)
        data = result.to_dict()
        
        assert data["Company"] == sample_analysis_data["Company"]
        assert data["Problem"] == sample_analysis_data["Problem"]
        assert "Sources" in data
    
    def test_missing_fields_default_to_empty(self):
        """Test that missing fields default to empty strings."""
        minimal_data = {"Company": "TestCo"}
        result = AnalysisResult(minimal_data)
        
        assert result.company == "TestCo"
        assert result.tagline == ""
        assert result.problem == ""
        assert result.sources == []


