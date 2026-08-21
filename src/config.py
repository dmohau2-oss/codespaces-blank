"""Configuration module for the data processing app."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

def resolve_input_file() -> str:
    """Pick a configured input file or fall back to bundled sample data."""
    configured = os.getenv("INPUT_FILE")
    sample_input = str(DATA_DIR / "sample_input.csv")

    if configured and Path(configured).exists():
        return str(configured)

    return sample_input


# Configuration settings
class Config:
    """Application configuration."""

    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    INPUT_FILE = resolve_input_file()
    OUTPUT_FILE = os.getenv("OUTPUT_FILE", str(OUTPUT_DIR / "output.csv"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # Data processing settings
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
    ENCODING = os.getenv("ENCODING", "utf-8")
