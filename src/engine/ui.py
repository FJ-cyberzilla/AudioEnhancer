"""
Rich-based Terminal UI implementation.
Handles themes, layouts, and strictly visual components.
"""

from typing import Final

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich.table import Table
from rich.theme import Theme
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)

# Constants
VINTAGE_ORANGE: Final[str] = "dark_orange"


class UIManager:
    """Encapsulates all standard output and CLI interactions."""

    def __init__(self) -> None:
        self.theme = Theme(
            {
                "primary": VINTAGE_ORANGE,
                "secondary": "orange3",
                "info": "cyan",
                "success": "bold green",
                "error": "bold red",
                "warning": "bold yellow",
            }
        )
        # Force interaction with the terminal emulator to handle resizing gracefully
        self.console = Console(theme=self.theme, force_terminal=True, soft_wrap=True)

    def print_branding(self, message: str) -> None:
        """Prints FJ™ - Cyberzilla branding."""
        self.console.print(f"\n[primary]✨ FJ™ - Cyberzilla | {message} ✨[/primary]\n")

    def draw_banner(self) -> None:
        """Renders the SOTA 2026 application banner."""
        self.console.clear()
        banner_text = (
            "==========================================================\n"
            "   ███▄    █  ▓█████  ▒██   ██▒ ██▓███   ██▀███   ▒█████  \n"
            "   ██ ▀█   █  ▓█   ▀  ▒▒ █ █ ▒░▓██░  ██▒▓██ ▒ ██▒▒██▒  ██▒\n"
            "  ▓██  ▀█ ██▒▒███    ░░  █   ░▓██░ ██▓▒▓██ ░▄█ ▒▒██░  ██▒\n"
            "  ▓██▒  ▐▌██▒▒▓█  ▄   ░ █ █ ▒ ▒██▄█▓▒ ▒▒██▀▀█▄  ▒██   ██░\n"
            "  ▒██░   ▓██░░▒████▒ ▒██▒ ▒██▒▒██▒ ░  ░░██▓ ▒██▒░ ████▓▒░\n"
            "==========================================================\n"
            "   MODULAR AUDIO MASTERING PIPELINE  •  SOTA 2026 EDITION \n"
        )
        banner = Text(banner_text, style=f"bold {VINTAGE_ORANGE}", justify="center")
        self.console.print(Panel(banner, border_style=VINTAGE_ORANGE, padding=(1, 2)))
        self.console.print()

    def get_main_menu_choice(self) -> str:
        """Displays main menu and captures validated input."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style="secondary")
        table.add_column(style="white")
        table.add_row("[ 1 ]", "Enhance Single File")
        table.add_row("[ 2 ]", "Batch Enhance Directory")
        table.add_row("[ 3 ]", "Exit Pipeline")

        self.console.print(
            Panel(
                table,
                title=f"[{VINTAGE_ORANGE}]Operation Mode[/{VINTAGE_ORANGE}]",
                border_style=VINTAGE_ORANGE,
                expand=False,
            )
        )
        return Prompt.ask(
            f"\n[{VINTAGE_ORANGE}]Awaiting Command[/{VINTAGE_ORANGE}]",
            choices=["1", "2", "3"],
            default="1",
        )

    def get_quality_selection(self) -> str:
        """Displays quality profile menu and captures validated input."""
        return Prompt.ask(
            f"\n[{VINTAGE_ORANGE}]Select Quality Profile[/{VINTAGE_ORANGE}]",
            choices=["Studio", "Mastering", "Balanced"],
            default="Studio",
        )

    def create_progress_context(self) -> Progress:
        """Returns a configured Rich Progress instance."""
        return Progress(
            SpinnerColumn(spinner_name="dots", style=VINTAGE_ORANGE),
            TextColumn("[bold white]{task.description}"),
            BarColumn(complete_style=VINTAGE_ORANGE, finished_style="green"),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=self.console,
            expand=True,
        )

    def print_error(self, message: str) -> None:
        """Prints a formatted error message to the console with a failure indicator."""
        self.console.print(f"\n[error]❌ ERROR:[/error] {message}")

    def print_success(self, message: str) -> None:
        """Prints a formatted success message to the console with a checkmark."""
        self.console.print(f"\n[success]✅ SUCCESS:[/success] {message}")

    def pause(self) -> None:
        """Pauses execution until the user presses Enter."""
        Prompt.ask(
            f"\n[{VINTAGE_ORANGE}]Press Enter to continue[/{VINTAGE_ORANGE}]",
            default="",
        )
