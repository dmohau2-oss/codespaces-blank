"""Main entry point for the data processing application."""

import argparse
import logging
from pathlib import Path
import sys

import pandas as pd

# Make direct execution (`python src/main.py`) use the same package imports
# as module execution (`python -m src.main`).
if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import Config
from src.processor import DataProcessor

# Configure logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def configure_logging(log_file: str | None = None):
    """Configure root logging with optional file output."""
    log_path = log_file or Config.OUTPUT_FILE.replace(".csv", ".log")
    log_dir = log_path.rsplit("/", 1)[0] if "/" in log_path else "."
    import os
    os.makedirs(log_dir, exist_ok=True)

    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_path, encoding="utf-8"))

    logging.basicConfig(
        level=Config.LOG_LEVEL,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers,
        force=True,
    )


def main(argv=None):
    """Run the main application."""
    parser = argparse.ArgumentParser(description="Process CSV data and print a summary.")
    parser.add_argument("--input", dest="input_file", default=Config.INPUT_FILE, help="Path to the input CSV file")
    parser.add_argument("--output", dest="output_file", default=Config.OUTPUT_FILE, help="Path to the output CSV file")
    parser.add_argument("--group-by", dest="group_by", default=None, help="Optional column to group summary totals and averages by")
    parser.add_argument("--no-clean", action="store_true", help="Skip data cleaning steps")
    parser.add_argument("--summary-json", dest="summary_json", default=None, help="Optional path to export the summary as JSON")
    parser.add_argument("--log-file", dest="log_file", default=None, help="Optional file path for application logging")
    parser.add_argument("--validate-only", action="store_true", help="Validate the input data without saving processed output")
    parser.add_argument("--output-json", dest="output_json", default=None, help="Optional path to export the processed data as JSON")
    args = parser.parse_args(argv)

    try:
        configure_logging(args.log_file)
        logger = logging.getLogger(__name__)
        logger.info("Starting data processing application")

        processor = DataProcessor(input_file=args.input_file)

        if args.validate_only:
            if not processor.validate_data(pd.read_csv(args.input_file), required_columns=["value"]):
                logger.warning("Validation failed for %s", args.input_file)
                return 1
            print(f"Validation successful for {args.input_file}")
            logger.info("Validation complete without writing output files")
            return 0

        result_df = processor.process(
            validate=True,
            clean=not args.no_clean,
            output_file=args.output_file if not args.output_json else None,
            required_columns=["value"],
        )

        if result_df.empty:
            logger.warning("Processing resulted in empty DataFrame")
            return 1

        if args.output_json:
            import json
            output_dir = args.output_json.rsplit("/", 1)[0] if "/" in args.output_json else "."
            import os
            os.makedirs(output_dir, exist_ok=True)
            with open(args.output_json, "w", encoding="utf-8") as fh:
                json.dump(result_df.to_dict(orient="records"), fh, indent=2)
            print(f"Processed data exported to JSON: {args.output_json}")

        summary = processor.summarise_data(result_df, group_by=args.group_by if args.group_by in result_df.columns else None)
        print(f"Rows processed: {summary['row_count']}")
        print(f"Value column: {summary['value_column']}")
        print(f"Total: {summary['total']:.2f}")
        print(f"Average: {summary['average']:.2f}")
        print(f"Min: {summary['min']:.2f}")
        print(f"Max: {summary['max']:.2f}")
        print(f"Median: {summary['median']:.2f}")
        print(f"Std Dev: {summary['stddev']:.2f}")

        if summary["group_summary"]:
            print("Grouped summary:")
            for group_name, group_data in summary["group_summary"].items():
                print(f"  {group_name}: total={group_data['total']:.2f}, average={group_data['average']:.2f}, median={group_data['median']:.2f}, count={group_data['count']}")

        if args.summary_json:
            import json
            output_dir = args.summary_json.rsplit("/", 1)[0] if "/" in args.summary_json else "."
            import os
            os.makedirs(output_dir, exist_ok=True)
            with open(args.summary_json, "w", encoding="utf-8") as fh:
                json.dump(summary, fh, indent=2)
            print(f"Summary JSON exported to: {args.summary_json}")

        logger.info(f"Processing complete. Output saved to {args.output_file}")
        logger.info(f"Processed {len(result_df)} rows")

        return 0

    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.error(f"Application error: {str(e)}", exc_info=True)
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
