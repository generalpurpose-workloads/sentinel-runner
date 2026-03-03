# sentinel-runner

> Lightweight build tool tool for cli utilities workflows

Built with argparse, rich, pathlib.

## Features

- Fast batch processing with configurable workers
- Environment-based configuration with sensible defaults
- Structured logging and error handling
- Retry logic with exponential backoff

## Installation

```bash
git clone https://github.com/user/sentinel-runner.git
cd sentinel-runner
pip install -r requirements.txt
```

## Quick Start

```bash
# Basic usage
python main.py --config config.toml

# With options
python main.py --verbose --output-dir ./results
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `LOG_LEVEL` | `INFO` | Logging verbosity |
| `BATCH_SIZE` | `100` | Items per batch |
| `MAX_WORKERS` | `4` | Parallel workers |
| `OUTPUT_DIR` | `./output` | Output directory |

## License

MIT License — see [LICENSE](LICENSE) for details.
