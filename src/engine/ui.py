"""
Rich-based Terminal UI implementation.
Handles themes, layouts, and strictly visual components.
"""

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

class UIManager:
    """Encapsulates all standard output and CLI interactions."""
    
    def __init__(self) -> None:
        self.theme = Theme({
            "primary": "dark_orange",
            "secondary": "orange3",
            "info": "cyan",
            "success": "bold green",
            "error": "bold red",
            "warning": "bold yellow"
        })
        self.console = Console(theme=self.theme)

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
        banner = Text(banner_text, style="bold #FF8C00", justify="center")
        self.console.print(Panel(banner, border_style="#FF4500", padding=(1, 2)))
        self.console.print()

    def get_main_menu_choice(self) -> str:
        """Displays main menu and captures validated input."""
        table = Table(show_header=False, box=None, padding=(0, 2))
        table.add_column(style="secondary")
        table.add_column(style="white")
        table.add_row("[ 1 ]", "Enhance Single File")
        table.add_row("[ 2 ]", "Batch Enhance Directory")
        table.add_row("[ 3 ]", "Exit Pipeline")
        
        self.console.print(Panel(table, title="[primary]Operation Mode", border_style="primary", expand=False))
        return Prompt.ask("\n[primary]Awaiting Command", choices=["1", "2", "3"], default="1")

    def create_progress_context(self) -> Progress:
        """Returns a configured Rich Progress instance."""
        return Progress(
            SpinnerColumn(spinner_name="dots", style="primary"),
            TextColumn("[bold white]{task.description}"),
            BarColumn(complete_style="dark_orange", finished_style="green"),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=self.console,
            expand=True
        )

    def print_error(self, message: str) -> None:
        self.console.print(f"\n[error]ERROR:[/error] {message}")

    def print_success(self, message: str) -> None:
        self.console.print(f"\n[success]SUCCESS:[/success] {message}")
        
    def pause(self) -> None:
        Prompt.ask("\n[secondary]Press Enter to continue[/secondary]", default="")
