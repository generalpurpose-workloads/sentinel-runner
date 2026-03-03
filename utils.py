"""
Utility functions for sentinel_runner.
"""
import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any, Optional


def compute_checksum(filepath: str, algorithm: str = "sha256") -> str:
    """Compute file checksum without loading entire file into memory."""
    h = hashlib.new(algorithm)
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_json_load(path: str, default: Any = None) -> Any:
    """Load JSON file with graceful error handling."""
    try:
        with open(path) as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        return default


def ensure_directory(path: str) -> Path:
    """Create directory tree if it does not exist."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def format_size(num_bytes: int) -> str:
    """Format byte count as human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if abs(num_bytes) < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} PB"


def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable string."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes}m {secs:.0f}s"


class Timer:
    """Context manager for timing operations."""

    def __init__(self, label: str = ""):
        self.label = label
        self.elapsed = 0.0

    def __enter__(self):
        self._start = time.monotonic()
        return self

    def __exit__(self, *args):
        self.elapsed = time.monotonic() - self._start
        if self.label:
            print(f"[{self.label}] {self.elapsed:.3f}s")


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Decorator for retrying operations with exponential backoff."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        wait = delay * (backoff ** attempt)
                        time.sleep(wait)
            raise last_error
        return wrapper
    return decorator
