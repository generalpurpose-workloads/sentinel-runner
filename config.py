"""
Configuration management for sentinel_runner.
"""
import os
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Config:
    """
    Application configuration.
    
    Values can be overridden via environment variables.
    """

    # Core settings
    app_name: str = "sentinel_runner"
    debug: bool = False
    log_level: str = "INFO"

    # Processing
    batch_size: int = 100
    max_workers: int = 4
    timeout_seconds: int = 30
    max_retries: int = 3

    # Storage paths
    data_dir: str = "./data"
    output_dir: str = "./output"
    cache_dir: str = "./.cache"

    # Feature flags
    enable_cache: bool = True
    dry_run: bool = False

    # Optional integrations
    api_url: Optional[str] = None
    api_key: Optional[str] = None

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        return cls(
            debug=os.environ.get("DEBUG", "0") == "1",
            log_level=os.environ.get("LOG_LEVEL", "INFO"),
            batch_size=int(os.environ.get("BATCH_SIZE", "100")),
            max_workers=int(os.environ.get("MAX_WORKERS", "4")),
            timeout_seconds=int(os.environ.get("TIMEOUT", "30")),
            data_dir=os.environ.get("DATA_DIR", "./data"),
            output_dir=os.environ.get("OUTPUT_DIR", "./output"),
            cache_dir=os.environ.get("CACHE_DIR", "./.cache"),
            api_url=os.environ.get("API_URL"),
            api_key=os.environ.get("API_KEY"),
        )
