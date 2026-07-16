"""Strictly typed configuration management using Pydantic."""

from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import Field

class EnhancerConfig(BaseSettings):
    """
    SOTA Configuration model. 
    Can be overridden by Environment variables (e.g., NEXUS_TARGET_BITRATE).
    """
    quality_profile: Literal["Broadcast", "Studio", "Mastering"] = Field(
        default="Studio", 
        description="The DSP chain complexity profile."
    )
    target_bitrate: int = Field(
        default=320000, 
        description="Target MP3 bitrate in bps."
    )
    chunk_size_frames: int = Field(
        default=44100 * 2, # ~2 seconds at 44.1kHz
        description="Frames per processing chunk to maintain low RAM footprint."
    )
    output_suffix: str = Field(
        default="_nexus_master", 
        description="Appended to processed filenames."
    )

    class Config:
        env_prefix = "NEXUS_"
