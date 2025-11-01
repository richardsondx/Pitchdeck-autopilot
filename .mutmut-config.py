"""
Mutation testing configuration for mutmut.
"""

def pre_mutation(context):
    """Skip mutations in certain files or lines."""
    # Skip mutations in UI/display code
    if 'cli_ui.py' in context.filename:
        # Only test critical UI logic
        if context.current_line_index < 50:  # Skip most UI functions
            context.skip = True
    
    # Skip mutations in __init__ files
    if '__init__.py' in context.filename:
        context.skip = True
    
    # Skip mutations in main entry point (tested via integration)
    if 'main.py' in context.filename:
        # Only test core orchestration logic
        pass


# Paths to mutate (focus on core logic)
paths_to_mutate = [
    'deckbrief/text_cleaner.py',
    'deckbrief/ai_analyzer.py',
    'deckbrief/markdown_builder.py',
    'deckbrief/deck_parser.py',
]

# Test command
tests_dir = 'tests/'
runner = 'python -m pytest -x --tb=short'


