"""Configuration management for Nexus Audio Enhancer."""

from pydantic_settings import BaseSettings


class EnhancerConfig(BaseSettings):
    """
    Application configuration using Pydantic Settings.
    Environment variables (e.g. NEXUS_OUTPUT_SUFFIX) will override defaults.
    """

    output_suffix: str = "_enhanced"
    quality_profile: str = "Studio"
    chunk_size_frames: int = 44100

    def get_config_summary(self) -> str:
        """Returns a summary of the current configuration."""
        return f"Profile: {self.quality_profile}, Suffix: {self.output_suffix}"

    def get_chunk_size(self) -> int:
        """Returns the chunk size."""
        return self.chunk_size_frames

    # pylint: disable=too-few-public-methods
    class Config:
        """Pydantic configuration."""

        env_prefix = "NEXUS_"

    def get_prefix(self) -> str:
        """Returns the env prefix."""
        return self.Config.env_prefix
