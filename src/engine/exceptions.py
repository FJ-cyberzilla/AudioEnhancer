"""Domain-specific exceptions for Nexus Audio."""

class NexusError(Exception):
    """Base exception for all Nexus-related errors."""
    pass

class AudioProcessingError(NexusError):
    """Raised when the DSP engine fails to process an audio stream."""
    pass

class ConfigurationError(NexusError):
    """Raised when the provided configuration is invalid."""
    pass

class FileIOError(NexusError):
    """Raised when audio files cannot be read or written."""
    pass
