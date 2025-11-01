"""
CLI UI Module - Premium terminal experience with progress bars and styling.
"""

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.panel import Panel
from rich.text import Text
import time
from typing import Optional

console = Console()


def print_banner(file_path: str, mode: str = "Enriched"):
    """Display the application banner."""
    banner = Text()
    banner.append("🚀 PitchDeck Autopilot v1.0\n", style="bold cyan")
    banner.append("─" * 60 + "\n", style="blue")
    banner.append(f"📂 Input: {file_path}\n", style="white")
    banner.append(f"🧠 Mode: {mode}\n", style="white")
    banner.append("─" * 60, style="blue")
    
    console.print(banner)
    console.print()


def print_divider():
    """Print a visual divider."""
    console.print("─" * 60, style="blue")


def print_success(message: str):
    """Print a success message in green."""
    console.print(f"✅ {message}", style="bold green")


def print_error(message: str):
    """Print an error message in red."""
    console.print(f"❌ {message}", style="bold red")


def print_warning(message: str):
    """Print a warning message in yellow."""
    console.print(f"⚠️  {message}", style="bold yellow")


def print_info(message: str):
    """Print an info message."""
    console.print(f"ℹ️  {message}", style="cyan")


def print_stage(icon: str, message: str):
    """Print a processing stage message."""
    console.print(f"{icon} {message}", style="bold white")


def print_completion(output_path: str, elapsed_time: float):
    """Print completion message with output path and timing."""
    console.print()
    print_divider()
    print_success("Analysis complete!")
    console.print(f"📁 Output saved to: [cyan]{output_path}[/cyan]")
    console.print()
    console.print(f"⏱️  Total time: {format_time(elapsed_time)}", style="dim")
    print_divider()


def format_time(seconds: float) -> str:
    """Format elapsed time in a human-readable way."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    return f"{minutes}m {remaining_seconds}s"


def create_progress_bar() -> Progress:
    """Create a configured progress bar."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    )


def simulate_progress(message: str, steps: int = 10, delay: float = 0.1):
    """Simulate a progress bar for a task."""
    with create_progress_bar() as progress:
        task = progress.add_task(message, total=steps)
        for _ in range(steps):
            time.sleep(delay)
            progress.update(task, advance=1)


def print_debug_section(title: str, content: str, max_lines: int = 50):
    """Print debug information in a formatted panel."""
    lines = content.split('\n')
    if len(lines) > max_lines:
        truncated_content = '\n'.join(lines[:max_lines]) + f"\n\n... ({len(lines) - max_lines} more lines)"
    else:
        truncated_content = content
    
    panel = Panel(
        truncated_content,
        title=f"[bold yellow]🐛 {title}[/bold yellow]",
        border_style="yellow",
        expand=False
    )
    console.print(panel)
    console.print()


def print_extraction_summary(total_slides: int, ocr_count: int):
    """Print extraction summary."""
    message = f"✅ {total_slides} slides extracted"
    if ocr_count > 0:
        message += f" (OCR used on {ocr_count} slides)"
    console.print(message, style="green")


def print(text: str = ""):
    """Print a blank line or text."""
    console.print(text)

