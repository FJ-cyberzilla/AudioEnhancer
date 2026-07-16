### Nexus Audio Processor 

[![CodeQL Advanced](https://github.com/FJ-cyberzilla/AudioEnhancer/actions/workflows/codeql.yml/badge.svg)](https://github.com/FJ-cyberzilla/AudioEnhancer/actions/workflows/codeql.yml)
- (2026 SOTA Edition)

## Overview
Nexus is a modular, high-performance audio mastering pipeline designed for 2026 production workflows. Unlike consumer-grade enhancers, Nexus provides stream-based DSP processing, ensuring that memory usage remains constant even when processing multi-gigabyte audio assets.

## Technical Specifications

Engine: Spotify Pedalboard (C++ backend)
Concurrency: Multi-threaded I/O with GIL-bypass

## Architecture: Domain-Driven Design (DDD) with Dependency Injection

## Configuration: Pydantic-validated environment variables

## Toolchain: uv managed
Installation
Ensure uv is installed.

- Clone the repository
git clone <repo-url>
cd nexus-enhancer

- Sync dependencies and build environment
uv sync

- Execute the pipeline
uv run nexus

- Production Pipeline
Config Layer: Environment variables (e.g., NEXUS_TARGET_BITRATE=320000) override defaults.
DSP Layer: The AudioEngine orchestrates the pedalboard chain.
UI Layer: The UIManager reports status via a non-blocking generator loop.
