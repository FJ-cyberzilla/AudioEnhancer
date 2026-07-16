"""
Application Controller orchestrating configuration, UI, and DSP engines.
Acts as the main entry point via pyproject.toml scripts.
"""

import sys
from pathlib import Path
import logging
from concurrent.futures import ThreadPoolExecutor

# Make sure pedalboard doesn't log too verbosely
logging.getLogger("pedalboard").setLevel(logging.ERROR)

from nexus.config import EnhancerConfig
from nexus.dsp import AudioEngine
from nexus.ui import UIManager
from nexus.exceptions import NexusError
from pedalboard.io import AudioFile

class NexusCLI:
    """Dependency-injected Controller mapping user actions to domain logic."""

    def __init__(self, config: EnhancerConfig, engine: AudioEngine, ui: UIManager) -> None:
        self.config = config
        self.engine = engine
        self.ui = ui

    def run(self) -> None:
        """Main application loop."""
        try:
            while True:
                self.ui.draw_banner()
                choice = self.ui.get_main_menu_choice()
                
                if choice == "1":
                    self._process_single_file()
                elif choice == "2":
                    self._process_batch()
                elif choice == "3":
                    self.ui.console.print("\n[primary]Gracefully shutting down pipeline.[/primary]")
                    break
        except KeyboardInterrupt:
            self.ui.console.print("\n\n[warning]Pipeline interrupted by operator. Exiting.[/warning]")
            sys.exit(0)

    def _process_single_file(self) -> None:
        """Handles single file ingestion and processing via DSP Generator."""
        input_str = self.ui.console.input("\n[primary]Enter source audio file path:[/primary] ")
        input_path = Path(input_str.strip('\"\''))
        
        if not input_path.exists() or not input_path.is_file():
            self.ui.print_error("Invalid file path provided.")
            self.ui.pause()
            return

        output_path = input_path.parent / f"{input_path.stem}{self.config.output_suffix}.mp3"
        
        try:
            # SOTA metadata extraction before processing
            with AudioFile(str(input_path)) as f:
                total_frames = f.frames
            
            with self.ui.create_progress_context() as progress:
                task_id = progress.add_task(
                    f"[orange3]Mastering {input_path.name}...", 
                    total=total_frames
                )
                
                # Consume the generator yielded by the DSP Engine
                for processed_frames in self.engine.process_file(input_path, output_path):
                    progress.update(task_id, advance=processed_frames)
                    
                progress.update(task_id, description="[green]Mastering Completed")
                
            self.ui.print_success(f"Artifact generated at: {output_path}")
            
        except NexusError as e:
            self.ui.print_error(str(e))
        except Exception as e:
            self.ui.print_error(f"Unhandled system fault: {e}")
            
        self.ui.pause()

    def _process_batch(self) -> None:
        """Batch processing using a ThreadPool for concurrent I/O & DSP."""
        dir_str = self.ui.console.input("\n[primary]Enter source directory path:[/primary] ")
        dir_path = Path(dir_str.strip('\"\''))
        
        if not dir_path.is_dir():
            self.ui.print_error("Invalid directory path provided.")
            self.ui.pause()
            return
            
        files = list(dir_path.glob("*.mp3")) + list(dir_path.glob("*.wav"))
        if not files:
            self.ui.print_error("No supported audio files found in directory.")
            self.ui.pause()
            return

        self.ui.console.print(f"\n[info]Found {len(files)} files. Initializing concurrent pipeline...[/info]")
        
        # Concurrency Model: ThreadPoolExecutor is safe here as I/O reading releases GIL,
        # and Pedalboard C++ DSP extensions also typically operate outside the GIL lock.
        with self.ui.create_progress_context() as progress:
            overall_task = progress.add_task("[orange3]Batch Pipeline Progress...", total=len(files))
            
            def process_target(file_path: Path) -> None:
                out = file_path.parent / f"{file_path.stem}{self.config.output_suffix}.mp3"
                # Consume generator to completion without UI updates per-file (to avoid terminal clutter)
                for _ in self.engine.process_file(file_path, out):
                    pass
                progress.advance(overall_task)

            with ThreadPoolExecutor(max_workers=4) as executor:
                # Map futures but we just wait for completion via context manager exit
                list(executor.map(process_target, files))
                
            progress.update(overall_task, description="[green]Batch Pipeline Completed")
            
        self.ui.print_success("All artifacts successfully generated.")
        self.ui.pause()

def main() -> None:
    """Application Entry Point."""
    config = EnhancerConfig()
    ui = UIManager()
    
    try:
        engine = AudioEngine(config)
        app = NexusCLI(config, engine, ui)
        app.run()
    except Exception as e:
        ui.print_error(f"Fatal initialization failure: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
