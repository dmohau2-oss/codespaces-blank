"""Unit tests for the data processor module."""

import importlib
import os
import pytest
import pandas as pd
import tempfile
from pathlib import Path
import src.config as config_module
from src.processor import DataProcessor


@pytest.fixture
def sample_data():
    """Create sample test data."""
    data = {
        'id': [1, 2, 3, 4, 5],
        'name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
        'value': [10.5, 20.3, 15.8, 25.2, 30.1]
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_csv(sample_data):
    """Create temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(
        mode='w',
        suffix='.csv',
        delete=False,
        encoding='utf-8'
    ) as f:
        sample_data.to_csv(f, index=False)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink()


def test_processor_initialization():
    """Test processor initialization."""
    processor = DataProcessor()
    assert processor.data is None
    assert processor.input_file is not None


def test_default_input_file_uses_sample_data_when_input_csv_missing(tmp_path):
    """The app should fall back to sample_input.csv when no valid input file is configured."""
    original_input = os.environ.get("INPUT_FILE")
    os.environ["INPUT_FILE"] = str(tmp_path / "missing.csv")

    try:
        importlib.reload(config_module)
        input_path = Path(config_module.Config.INPUT_FILE)
        assert input_path.exists()
        assert input_path.name == "sample_input.csv"
    finally:
        if original_input is None:
            os.environ.pop("INPUT_FILE", None)
        else:
            os.environ["INPUT_FILE"] = original_input
        importlib.reload(config_module)


def test_validate_data_with_valid_dataframe(sample_data):
    """Test data validation with valid DataFrame."""
    processor = DataProcessor()
    assert processor.validate_data(sample_data) is True


def test_validate_data_with_empty_dataframe():
    """Test data validation with empty DataFrame."""
    processor = DataProcessor()
    empty_df = pd.DataFrame()
    assert processor.validate_data(empty_df) is False


def test_clean_data(sample_data):
    """Test data cleaning."""
    processor = DataProcessor()
    
    # Add duplicates
    df_with_dupes = pd.concat([sample_data, sample_data.iloc[[0]]], ignore_index=True)
    
    cleaned = processor.clean_data(df_with_dupes)
    
    # Should have removed duplicates
    assert len(cleaned) == len(sample_data)


def test_summary_calculates_totals_and_averages(sample_data):
    """Summary should compute totals and averages over the numeric value column."""
    processor = DataProcessor()
    summary = processor.summarise_data(sample_data)

    assert summary["row_count"] == len(sample_data)
    assert summary["value_column"] == "value"
    assert summary["total"] == pytest.approx(101.9)
    assert summary["average"] == pytest.approx(20.38)


def test_grouped_summary_by_category():
    """Grouped summaries should aggregate totals and averages per category."""
    df = pd.DataFrame(
        {
            "category": ["A", "A", "B", "B"],
            "value": [10.0, 20.0, 30.0, 40.0],
        }
    )
    processor = DataProcessor()
    summary = processor.summarise_data(df, group_by="category")

    assert summary["grouped_by"] == "category"
    assert summary["group_summary"]["A"]["total"] == pytest.approx(30.0)
    assert summary["group_summary"]["A"]["average"] == pytest.approx(15.0)
    assert summary["group_summary"]["B"]["total"] == pytest.approx(70.0)
    assert summary["group_summary"]["B"]["average"] == pytest.approx(35.0)


def test_validate_data_requires_expected_columns(sample_data):
    """Validation should fail when required columns are missing."""
    processor = DataProcessor()
    bad_df = sample_data.drop(columns=["value"])

    assert processor.validate_data(bad_df, required_columns=["value"]) is False


def test_summarise_data_can_export_json(sample_data):
    """Summary output should be serialisable to JSON for export."""
    processor = DataProcessor()
    summary = processor.summarise_data(sample_data)

    assert isinstance(summary, dict)
    assert summary["row_count"] == len(sample_data)
    assert summary["total"] == pytest.approx(101.9)


def test_summarise_data_includes_extra_aggregations(sample_data):
    """Summary should include min, max, median, and standard deviation values."""
    processor = DataProcessor()
    summary = processor.summarise_data(sample_data)

    assert summary["min"] == pytest.approx(10.5)
    assert summary["max"] == pytest.approx(30.1)
    assert summary["median"] == pytest.approx(20.3)
    assert summary["stddev"] == pytest.approx(sample_data["value"].std(ddof=1))


def test_main_cli_accepts_input_output_group_and_log_file(tmp_path, sample_data):
    """The CLI should accept the new summary and logging options without crashing."""
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    summary_path = tmp_path / "summary.json"
    log_path = tmp_path / "logs" / "app.log"
    sample_data.to_csv(input_path, index=False)

    from src.main import main

    exit_code = main([
        "--input", str(input_path),
        "--output", str(output_path),
        "--group-by", "name",
        "--summary-json", str(summary_path),
        "--log-file", str(log_path),
    ])

    assert exit_code == 0
    assert output_path.exists()
    assert summary_path.exists()
    assert log_path.exists()


def test_main_cli_validate_only_mode(tmp_path, sample_data):
    """Validate-only mode should check validity without writing output files."""
    input_path = tmp_path / "input.csv"
    output_path = tmp_path / "output.csv"
    sample_data.to_csv(input_path, index=False)

    from src.main import main

    exit_code = main(["--input", str(input_path), "--validate-only", "--output", str(output_path)])

    assert exit_code == 0
    assert not output_path.exists()


def test_main_cli_output_json_mode(tmp_path, sample_data):
    """The CLI should be able to export the processed data as JSON."""
    input_path = tmp_path / "input.csv"
    output_json = tmp_path / "processed.json"
    sample_data.to_csv(input_path, index=False)

    from src.main import main

    exit_code = main(["--input", str(input_path), "--output-json", str(output_json)])

    assert exit_code == 0
    assert output_json.exists()


def test_save_data(sample_data):
    """Test saving data to file."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "test_output.csv"
        
        processor = DataProcessor()
        processor.save_data(sample_data, str(output_path))
        
        # Verify file was created and contains data
        assert output_path.exists()
        
        loaded = pd.read_csv(output_path)
        assert len(loaded) == len(sample_data)
        assert list(loaded.columns) == list(sample_data.columns)
