"""
Application Controller orchestrating configuration, UI, and DSP engines.
Acts as the main entry point via pyproject.toml scripts.
"""

import logging
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from types import FrameType
from typing import Any, Final

from pedalboard.io import AudioFile
from rich.progress import Progress

from engine.exceptions import NexusError
from engine.ui import UIManager
from models.dsp import AudioEngine
from nexus.config import EnhancerConfig

# Make sure pedalboard doesn't log too verbosely
logging.getLogger("pedalboard").setLevel(logging.ERROR)

# Branding constant
APP_NAME: Final[str] = "FJ™ - Cyberzilla"


class NexusCLI:
    """Dependency-injected Controller mapping user actions to domain logic."""

    def __init__(
        self, config: EnhancerConfig, engine: AudioEngine, ui: UIManager
    ) -> None:
        self.config = config
        self.engine = engine
        self.ui = ui
        # Handle signals for graceful shutdown (including Ctrl+Z)
        signal.signal(signal.SIGTSTP, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

    def _handle_signal(self, signum: int, frame: FrameType | None) -> None:
        """Handles signals to prevent abrupt crashes."""
        _ = frame
        self.ui.console.print(
            f"\n[warning]⚠️ Signal {signum} received. Shutting down...[/warning]"
        )
        self.shutdown()
        sys.exit(0)

    def run(self) -> None:
        """Main application loop."""
        self.ui.print_branding(f"{APP_NAME} - Started")
        try:
            while True:
                self.ui.draw_banner()
                choice = self.ui.get_main_menu_choice()

                if choice == "1":
                    self._process_single_file()
                elif choice == "2":
                    self._process_batch()
                elif choice == "3":
                    self.ui.console.print(
                        "\n[primary]Gracefully shutting down pipeline.[/primary]"
                    )
                    break
        except KeyboardInterrupt:
            self.ui.console.print(
                "\n\n[warning]❌ Pipeline interrupted by operator. Exiting.[/warning]"
            )
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.ui.print_error(f"Unexpected application failure: {e}")
        finally:
            self.shutdown()
            self.ui.print_branding(f"{APP_NAME} - Finished")

    def shutdown(self) -> None:
        """Performs cleanup tasks before exiting."""
        self.engine.reset_engine()

    def _process_single_file(self) -> None:
        """Handles single file ingestion and processing via DSP Generator."""
        input_str = self.ui.console.input(
            "\n[primary]Enter source audio file path:[/primary] "
        )
        input_path = Path(input_str.strip("\"'"))

        if not input_path.exists() or not input_path.is_file():
            self.ui.print_error("Invalid file path provided.")
            self.ui.pause()
            return

        quality = self.ui.get_quality_selection()
        self.config.quality_profile = quality
        self.engine.reset_engine()

        output_path = (
            input_path.parent / f"{input_path.stem}{self.config.output_suffix}.mp3"
        )

        try:
            # SOTA metadata extraction before processing
            with AudioFile(str(input_path)) as f:
                total_frames = f.frames

            with self.ui.create_progress_context() as progress:
                task_id = progress.add_task(
                    f"[orange3]Mastering {input_path.name} ({quality})...",
                    total=total_frames,
                )

                # Consume the generator yielded by the DSP Engine
                for processed_frames in self.engine.process_file(
                    input_path, output_path
                ):
                    progress.update(task_id, advance=processed_frames)

                progress.update(task_id, description="[green]Mastering Completed")

            self.ui.print_success(f"Artifact generated at: {output_path}")

        except NexusError as e:
            self.ui.print_error(f"Processing error: {e}")
        except RuntimeError as e:
            self.ui.print_error(f"DSP runtime failure: {e}")
        except Exception as e:  # pylint: disable=broad-exception-caught
            self.ui.print_error(f"Unhandled system fault: {e}")

        self.ui.pause()

    def _process_batch(self) -> None:
        """Batch processing using a ThreadPool for concurrent I/O & DSP."""
        dir_str = self.ui.console.input(
            "\n[primary]Enter source directory path:[/primary] "
        )
        dir_path = Path(dir_str.strip("\"'"))

        if not dir_path.is_dir():
            self.ui.print_error("Invalid directory path provided.")
            self.ui.pause()
            return

        files = list(dir_path.glob("*.mp3")) + list(dir_path.glob("*.wav"))
        if not files:
            self.ui.print_error("No supported audio files found in directory.")
            self.ui.pause()
            return

        quality = self.ui.get_quality_selection()
        self.config.quality_profile = quality
        self.engine.reset_engine()

        self.ui.console.print(
            f"\n[info]Found {len(files)} files. "
            f"Initializing concurrent pipeline ({quality})...[/info]"
        )

        with self.ui.create_progress_context() as progress:
            overall_task = progress.add_task(
                "[orange3]Batch Pipeline Progress...", total=len(files)
            )

            with ThreadPoolExecutor(max_workers=4) as executor:
                # Map futures but we just wait for completion via context manager exit
                for file_path in files:
                    executor.submit(
                        self._process_target_file, file_path, progress, overall_task
                    )

            progress.update(overall_task, description="[green]Batch Pipeline Completed")

        self.ui.print_success("All artifacts successfully generated.")
        self.ui.pause()

    def _process_target_file(
        self, file_path: Path, progress: Progress, task: Any
    ) -> None:
        """Helper to process a single file in the batch pipeline."""
        out = file_path.parent / f"{file_path.stem}{self.config.output_suffix}.mp3"
        # Consume generator to completion without UI updates per-file
        for _ in self.engine.process_file(file_path, out):
            pass
        progress.advance(task)


def main() -> None:
    """Application Entry Point."""
    config = EnhancerConfig()
    ui = UIManager()

    try:
        engine = AudioEngine(config)
        app = NexusCLI(config, engine, ui)
        app.run()
    except Exception as e:  # pylint: disable=broad-exception-caught
        ui.print_error(f"Fatal initialization failure: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
