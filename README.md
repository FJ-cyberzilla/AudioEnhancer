# Nexus Audio Enhancer

Nexus is a modular, high-performance audio mastering pipeline designed for professional-grade audio enhancement. Built with a focus on SOTA (State-of-the-Art) signal processing and memory-efficient I/O, it leverages Spotify's `pedalboard` library to deliver consistent, non-destructive mastering results for single files or large batch directories.

## Core Features

- **Non-Destructive Mastering Chain**: Implements a professionally curated DSP chain including noise gating, high-pass filtering, shelf EQ, compression, and limiting.
- **Memory-Safe Processing**: Utilizes chunked I/O generators to handle audio files of any size without loading entire files into memory.
- **Batch Processing**: Supports concurrent directory-wide batch processing using a thread-pooled architecture for maximum performance.
- **Professional UI (FJ™ - Cyberzilla)**: A rich, interactive terminal user interface featuring:
  - Interactive quality selection (`Studio`, `Mastering`, `Balanced`).
  - Real-time progress tracking with ETA.
  - Visual status indicators for success (✅) and failure (❌).
  - Robust terminal resizing and signal handling (`Ctrl+Z`, `SIGTERM`).
- **Configurable Profiles**: Easy customization via `pydantic-settings`, allowing environment variable overrides for suffixing, quality profiles, and chunk sizing.

## Architectural Design Principles

Nexus adheres to modern software engineering best practices:

1.  **Single Responsibility Principle (SRP)**: Clean separation between domain logic (`AudioEngine`), presentation (`UIManager`), and application control (`NexusCLI`).
2.  **Composition Over Inheritance**: The mastering chain is dynamically constructed through composition, ensuring flexibility and extensibility.
3.  **Dependency Injection**: Dependencies are injected into the controller, promoting testability and modularity.
4.  **Robust Error Handling**: Domain-specific exceptions ensure failures are handled gracefully at every layer of the pipeline.

## Installation

Ensure you have Python 3.11+ installed.

```bash
# Clone the repository
git clone https://github.com/your-username/AudioEnhancer.git
cd AudioEnhancer

# Install dependencies (recommended using a virtual environment)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Run the Application

```bash
python -m src.nexus.cli
```

### Configuration

Customize the application behavior by setting environment variables prefixed with `NEXUS_`:

- `NEXUS_OUTPUT_SUFFIX`: Custom suffix for processed files (default: `_enhanced`)
- `NEXUS_QUALITY_PROFILE`: Set mastering profile (`Studio` or `Mastering`)
- `NEXUS_CHUNK_SIZE_FRAMES`: Chunk size for processing (default: `44100`)

## Contributing

We welcome contributions! Please adhere to existing coding standards and ensure all new features are covered by tests.

---
*Built for SOTA 2026.*
