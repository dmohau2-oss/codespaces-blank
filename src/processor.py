"""Data processing module."""

import logging
from pathlib import Path
from typing import Optional
import pandas as pd
import numpy as np
from src.config import Config

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handle data processing and ETL operations."""
    
    def __init__(self, input_file: Optional[str] = None):
        """Initialize the data processor.
        
        Args:
            input_file: Path to input CSV file
        """
        self.input_file = input_file or Config.INPUT_FILE
        self.data = None

    def _resolve_input_file(self) -> str:
        """Return the existing input file path, falling back to the bundled sample CSV."""
        candidate = Path(self.input_file)
        if candidate.exists():
            return str(candidate)

        sample_file = Path(Config.PROJECT_ROOT) / "data" / "sample_input.csv"
        if sample_file.exists():
            logger.warning("Configured input file was not found; using bundled sample data instead.")
            self.input_file = str(sample_file)
            return str(sample_file)

        raise FileNotFoundError(f"Input file not found: {self.input_file}")
        
    def load_data(self) -> pd.DataFrame:
        """Load data from CSV file.
        
        Returns:
            Loaded DataFrame
            
        Raises:
            FileNotFoundError: If input file does not exist
        """
        try:
            input_path = self._resolve_input_file()
            logger.info(f"Loading data from {input_path}")
            self.data = pd.read_csv(
                input_path,
                encoding=Config.ENCODING,
                chunksize=Config.CHUNK_SIZE
            )
            logger.info("Data loaded successfully")
            return self.data
        except FileNotFoundError as e:
            logger.error(f"Input file not found: {self.input_file}")
            raise
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            raise
    
    def validate_data(self, df: pd.DataFrame, required_columns: Optional[list[str]] = None) -> bool:
        """Validate data quality and confirm required columns exist.
        
        Args:
            df: DataFrame to validate
            required_columns: Columns that must be present
            
        Returns:
            True if data is valid
        """
        logger.info("Validating data...")

        if df.empty:
            logger.warning("DataFrame is empty")
            return False

        if len(df.columns) == 0:
            logger.warning("DataFrame has no columns")
            return False

        if required_columns:
            missing = [column for column in required_columns if column not in df.columns]
            if missing:
                logger.warning("Missing required columns: %s", ", ".join(missing))
                return False

        logger.info(f"Data validation passed: {len(df)} rows, {len(df.columns)} columns")
        return True
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean and preprocess data.
        
        Args:
            df: DataFrame to clean
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("Cleaning data...")
        
        # Remove duplicates
        df = df.drop_duplicates()
        logger.info(f"Removed duplicates: {len(df)} rows remaining")
        
        # Handle missing values
        df = df.dropna()
        logger.info(f"Removed rows with missing values: {len(df)} rows remaining")
        
        return df
    
    def summarise_data(self, df: pd.DataFrame, group_by: Optional[str] = None) -> dict:
        """Compute totals and averages for numeric columns and optionally group by a category column."""
        if df.empty:
            return {
                "row_count": 0,
                "value_column": None,
                "total": 0.0,
                "average": 0.0,
                "min": 0.0,
                "max": 0.0,
                "median": 0.0,
                "stddev": 0.0,
                "grouped_by": group_by,
                "group_summary": {},
            }

        value_column = "value"
        if value_column not in df.columns:
            numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
            if not numeric_columns:
                raise ValueError("No numeric columns available for aggregation.")
            value_column = numeric_columns[0]

        series = df[value_column].astype(float)
        total = float(series.sum())
        average = float(series.mean())
        median = float(series.median())
        stddev = float(series.std(ddof=1)) if len(series) > 1 else 0.0

        summary = {
            "row_count": int(len(df)),
            "value_column": value_column,
            "total": total,
            "average": average,
            "min": float(series.min()),
            "max": float(series.max()),
            "median": median,
            "stddev": stddev,
            "grouped_by": group_by,
            "group_summary": {},
        }

        if group_by and group_by in df.columns:
            grouped = df.groupby(group_by, dropna=False)[value_column].agg(["sum", "mean", "median", "min", "max", "std", "count"]).reset_index()
            summary["group_summary"] = {
                str(row[group_by]): {
                    "total": float(row["sum"]),
                    "average": float(row["mean"]),
                    "median": float(row["median"]),
                    "min": float(row["min"]),
                    "max": float(row["max"]),
                    "stddev": float(row["std"]) if pd.notna(row["std"]) else 0.0,
                    "count": int(row["count"]),
                }
                for _, row in grouped.iterrows()
            }

        return summary

    def save_data(self, df: pd.DataFrame, output_file: Optional[str] = None) -> None:
        """Save processed data to CSV file.
        
        Args:
            df: DataFrame to save
            output_file: Path to output CSV file
        """
        output_path = output_file or Config.OUTPUT_FILE
        
        try:
            logger.info(f"Saving data to {output_path}")
            df.to_csv(output_path, index=False, encoding=Config.ENCODING)
            logger.info("Data saved successfully")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
            raise
    
    def process(
        self,
        validate: bool = True,
        clean: bool = True,
        output_file: Optional[str] = None,
        required_columns: Optional[list[str]] = None,
    ) -> pd.DataFrame:
        """Main processing pipeline.
        
        Args:
            validate: Whether to validate data
            clean: Whether to clean data
            output_file: Optional custom output path
            required_columns: Columns required for validation
            
        Returns:
            Processed DataFrame
        """
        logger.info("Starting data processing pipeline...")

        self.load_data()
        df = pd.concat(self.data, ignore_index=True)

        if validate and not self.validate_data(df, required_columns=required_columns):
            logger.warning("Data validation failed")
            return pd.DataFrame()

        if clean:
            df = self.clean_data(df)

        self.save_data(df, output_file=output_file)

        logger.info("Processing pipeline completed")
        return df
