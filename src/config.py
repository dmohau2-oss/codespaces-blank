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
    """Pick the best available input file, preferring valid configured paths and falling back to bundled sample data."""
    configured = os.getenv("INPUT_FILE")
    candidates = []

    if configured:
        candidates.append(configured)

    default_input = str(DATA_DIR / "input.csv")
    sample_input = str(DATA_DIR / "sample_input.csv")

    candidates.extend([default_input, sample_input])

    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)

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
