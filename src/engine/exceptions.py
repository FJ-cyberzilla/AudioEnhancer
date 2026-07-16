"""Domain-specific exceptions for Nexus Audio."""


class NexusError(Exception):
    """Base exception for all Nexus-related errors."""


class AudioProcessingError(NexusError):
    """Raised when the DSP engine fails to process an audio stream."""


class ConfigurationError(NexusError):
    """Raised when the provided configuration is invalid."""


class FileIOError(NexusError):
    """Raised when audio files cannot be read or written."""
