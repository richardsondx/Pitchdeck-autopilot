#!/usr/bin/env python3
"""
PitchDeck Autopilot - Main CLI Entry Point

Transform pitch decks into structured investment briefs.
"""

import click
import os
import sys
import time
from dotenv import load_dotenv

from deckbrief import __version__
from deckbrief.deck_parser import parse_deck, get_full_text
from deckbrief.text_cleaner import clean_text
from deckbrief.ai_analyzer import analyze_deck, create_fast_analysis
from deckbrief.markdown_builder import build_markdown, save_markdown, save_debug_info
from deckbrief import cli_ui


# Load environment variables
load_dotenv()


@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--fast', is_flag=True, help='Skip AI enrichment, fast extraction only')
@click.option('--debug', is_flag=True, help='Show raw extracted text and save debug files')
@click.option('--output-dir', default='output', help='Output directory for markdown files')
def main(file_path: str, fast: bool, debug: bool, output_dir: str):
    """
    Transform pitch decks into structured investment briefs.
    
    FILE_PATH: Path to the pitch deck (.pdf or .pptx)
    
    Examples:
    
      deckbrief pitch.pdf
      
      deckbrief presentation.pptx --fast
      
      deckbrief deck.pdf --debug
    """
    start_time = time.time()
    
    # Determine mode
    mode = "Fast Extraction" if fast else "Enriched (OpenRouter)"
    
    # Display banner
    cli_ui.print_banner(file_path, mode)
    
    try:
        # Stage 1: Extract slides
        cli_ui.print_stage("🔍", "Extracting slides...")
        time.sleep(0.15)  # Micro-delay for perceived quality
        
        try:
            slides, ocr_count = parse_deck(file_path)
        except ValueError as e:
            cli_ui.print_error(str(e))
            sys.exit(1)
        
        if not slides:
            cli_ui.print_error("No content could be extracted from the deck")
            sys.exit(1)
        
        cli_ui.print_extraction_summary(len(slides), ocr_count)
        cli_ui.print()
        
        # Get full text
        full_text = get_full_text(slides)
        
        if debug:
            cli_ui.print_debug_section("Raw Extracted Text", full_text, max_lines=30)
        
        # Stage 2: Clean content
        cli_ui.print_stage("🧹", "Cleaning text...")
        time.sleep(0.1)
        
        cleaned_text = clean_text(full_text)
        cli_ui.print_success("Text cleaned and normalized")
        cli_ui.print()
        
        # Stage 3: Analyze deck
        if fast:
            cli_ui.print_stage("⚡", "Creating fast summary (AI skipped)...")
            time.sleep(0.1)
            analysis = create_fast_analysis(cleaned_text, len(slides))
            cli_ui.print_success("Fast summary created")
        else:
            cli_ui.print_stage("🧠", "Analyzing content with OpenRouter...")
            
            api_key = os.getenv("OPENROUTER_API_KEY", "")
            
            try:
                analysis = analyze_deck(cleaned_text, api_key)
                cli_ui.print_success("AI analysis complete")
            except ValueError as e:
                cli_ui.print_error(str(e))
                sys.exit(1)
            except Exception as e:
                cli_ui.print_error(f"Analysis failed: {str(e)}")
                if debug:
                    cli_ui.print_debug_section("Error Details", str(e))
                sys.exit(1)
        
        cli_ui.print()
        
        # Stage 4: Generate Markdown
        cli_ui.print_stage("📄", "Writing structured Markdown brief...")
        time.sleep(0.1)
        
        markdown_content = build_markdown(analysis, len(slides), ocr_count)
        output_path = save_markdown(markdown_content, analysis.company, output_dir)
        
        cli_ui.print_success("Markdown brief generated")
        cli_ui.print()
        
        # Save debug info if requested
        if debug:
            save_debug_info(full_text, analysis.raw_response, "debug")
            cli_ui.print_info("Debug files saved to ./debug/")
            cli_ui.print()
        
        # Completion
        elapsed_time = time.time() - start_time
        cli_ui.print_completion(output_path, elapsed_time)
    
    except KeyboardInterrupt:
        cli_ui.print()
        cli_ui.print_warning("Process interrupted by user")
        sys.exit(130)
    
    except Exception as e:
        cli_ui.print()
        cli_ui.print_error(f"Unexpected error: {str(e)}")
        if debug:
            import traceback
            cli_ui.print_debug_section("Stack Trace", traceback.format_exc())
        sys.exit(1)


def cli():
    """Entry point for console script."""
    main()


if __name__ == "__main__":
    main()

