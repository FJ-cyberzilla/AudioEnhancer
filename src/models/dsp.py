"""
SOTA Digital Signal Processing Module.
Decoupled completely from the UI layer. Uses chunk-based I/O for massive files.
"""

import logging
from pathlib import Path
from collections.abc import Iterator
from pedalboard import (
    Pedalboard,
    NoiseGate,
    Compressor,
    HighpassFilter,
    LowShelfFilter,
    HighShelfFilter,
    Limiter,
)
from pedalboard.io import AudioFile
from nexus.config import EnhancerConfig
from nexus.exceptions import AudioProcessingError, FileIOError

logger = logging.getLogger(__name__)

class AudioEngine:
    """
    Professional Audio Engine wrapping Spotify's Pedalboard.
    Implements memory-safe chunked processing via generators.
    """
    def __init__(self, config: EnhancerConfig) -> None:
        self.config = config
        self.board = self._build_mastering_chain()

    def _build_mastering_chain(self) -> Pedalboard:
        """Constructs a non-destructive mastering chain based on the profile."""
        plugins = [
            NoiseGate(threshold_db=-45.0, ratio=1.5, release_ms=250),
            HighpassFilter(cutoff_frequency_hz=35.0),
        ]
        
        if self.config.quality_profile in ("Studio", "Mastering"):
            plugins.extend([
                LowShelfFilter(cutoff_frequency_hz=150.0, gain_db=1.2),
                HighShelfFilter(cutoff_frequency_hz=8000.0, gain_db=1.8),
            ])
            
        plugins.extend([
            Compressor(threshold_db=-14.0, ratio=3.0, attack_ms=5.0, release_ms=50.0),
            Limiter(threshold_db=-0.1)
        ])
        
        return Pedalboard(plugins)

    def process_file(self, input_path: Path, output_path: Path) -> Iterator[int]:
        """
        Processes an audio file efficiently in chunks.
        Yields the number of processed frames for UI consumption.
        """
        if not input_path.exists():
            raise FileIOError(f"Input file not found: {input_path}")

        try:
            with AudioFile(str(input_path)) as f_in:
                samplerate = f_in.samplerate
                channels = f_in.num_channels
                
                with AudioFile(
                    str(output_path), 
                    'w', 
                    samplerate=samplerate, 
                    num_channels=channels
                ) as f_out:
                    
                    while f_in.tell() < f_in.frames:
                        # Read chunk
                        chunk = f_in.read(self.config.chunk_size_frames)
                        if chunk.shape[1] == 0:
                            break
                            
                        # Apply DSP (Stateful processing via reset=False)
                        processed_chunk = self.board(chunk, samplerate, reset=False)
                        
                        # Write chunk
                        f_out.write(processed_chunk)
                        
                        # Yield progress to the caller (UI Layer)
                        yield chunk.shape[1]
                        
        except Exception as e:
            logger.exception("DSP chain failure")
            raise AudioProcessingError(f"Failed to process {input_path.name}: {str(e)}") from e
