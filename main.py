"""
sentinel_runner — build tool

A lightweight build tool tool for cli utilities workflows.
"""
import os
import sys
import logging
import argparse
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_logging(level: str = "INFO") -> None:
    """Configure structured logging."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="sentinel_runner: build tool tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-c", "--config",
        default=os.environ.get("CONFIG_PATH", "config.toml"),
        help="Path to configuration file",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without making changes",
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("OUTPUT_DIR", "./output"),
        help="Output directory (default: ./output)",
    )
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()
    setup_logging("DEBUG" if args.verbose else "INFO")
    
    logger.info("Starting %s...", "sentinel_runner")
    logger.info("Config: %s", args.config)
    
    try:
        from sentinel_runner.core import Processor
        
        processor = Processor(
            config_path=args.config,
            output_dir=args.output_dir,
            dry_run=args.dry_run,
        )
        result = processor.execute()
        
        logger.info(
            "Completed: processed %d items in %.2fs",
            result["items_processed"],
            result["elapsed_seconds"],
        )
        return 0
        
    except FileNotFoundError as e:
        logger.error("Configuration not found: %s", e)
        return 1
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        return 130
    except Exception as e:
        logger.exception("Fatal error: %s", e)
        return 1


if __name__ == "__main__":
    sys.exit(main())
