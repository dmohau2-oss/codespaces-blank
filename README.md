# Data Processing Application

A Python-based ETL application for processing and analyzing data with built-in validation and cleaning capabilities.

## Features

- **Data Loading**: Read CSV files with support for chunked processing
- **Data Validation**: Verify data quality and integrity
- **Data Cleaning**: Remove duplicates and handle missing values
- **Aggregations**: Compute totals and averages for numeric columns
- **CLI Interface**: Run the app from the command line with custom input/output paths
- **Error Handling**: Comprehensive logging and error reporting
- **Testing**: Unit tests included with pytest

## Project Structure

```
├── src/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── processor.py       # Main data processing logic
│   └── main.py            # Application entry point
├── tests/
│   ├── __init__.py
│   └── test_processor.py  # Unit tests
├── data/                  # Input data directory
├── output/                # Output data directory
├── requirements.txt       # Python dependencies
├── Dockerfile              # Container image definition
├── .dockerignore           # Docker build exclusions
├── .github/workflows/      # GitHub Actions CI/CD workflow
└── README.md             # This file
```

## Quick Start

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m src.main --input data/sample_input.csv --output output/processed.csv
```

This runs the processing pipeline, validates the data, and writes the cleaned results to the output file.

## Installation

1. **Clone or download the project**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root to customize settings:

```env
DEBUG=False
INPUT_FILE=data/input.csv
OUTPUT_FILE=output/output.csv
LOG_LEVEL=INFO
CHUNK_SIZE=1000
ENCODING=utf-8
```

## Usage

### Running the application:

```bash
python -m src.main
```

### Running with custom files:

```bash
python -m src.main --input data/sample_input.csv --output output/processed.csv
```

### Complete CLI usage examples

```bash
python -m src.main --help
```

```text
usage: src.main [-h] [--input INPUT_FILE] [--output OUTPUT_FILE]
               [--group-by GROUP_BY] [--no-clean]
               [--summary-json SUMMARY_JSON] [--log-file LOG_FILE]
               [--validate-only] [--output-json OUTPUT_JSON]

Process CSV data and print a summary.

options:
  -h, --help            show this help message and exit
  --input INPUT_FILE    Path to the input CSV file
  --output OUTPUT_FILE  Path to the output CSV file
  --group-by GROUP_BY   Optional column to group summary totals and averages by
  --no-clean            Skip data cleaning steps
  --summary-json SUMMARY_JSON
                        Optional path to export the summary as JSON
  --log-file LOG_FILE   Optional file path for application logging
  --validate-only       Validate the input data without saving processed output
  --output-json OUTPUT_JSON
                        Optional path to export the processed data as JSON
```

#### 1) Run the default pipeline
```bash
python -m src.main
```

#### 2) Process a custom input and save to a custom output
```bash
python -m src.main \
  --input data/sample_input.csv \
  --output output/processed.csv
```

#### 3) Group results by category and export summary JSON
```bash
python -m src.main \
  --input data/sample_input.csv \
  --output output/processed.csv \
  --group-by category \
  --summary-json output/summary.json
```

#### 4) Validate the file without writing output
```bash
python -m src.main --input data/sample_input.csv --validate-only
```

#### 5) Export processed data to JSON instead of CSV
```bash
python -m src.main \
  --input data/sample_input.csv \
  --output-json output/processed.json
```

#### 6) Skip cleaning and write logs to a file
```bash
python -m src.main \
  --input data/sample_input.csv \
  --output output/processed.csv \
  --no-clean \
  --log-file output/app.log
```

#### 7) Combine all options in one run
```bash
python -m src.main \
  --input data/sample_input.csv \
  --output output/processed.csv \
  --group-by category \
  --summary-json output/summary.json \
  --log-file output/app.log \
  --output-json output/processed.json
```

The CLI prints a summary including:

- row count
- value column used for aggregation
- total
- average
- min, max, median, and standard deviation
- grouped totals and averages when `--group-by` is provided

### Running tests:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_processor.py
```

## Docker

Build the image locally:

```bash
docker build -t data-processing-app .
```

Run the container and persist generated files in the local `output/` directory:

```bash
docker run --rm \
  -v "$PWD/output:/app/output" \
  data-processing-app \
  --input data/sample_input.csv \
  --output output/processed.csv \
  --group-by category \
  --summary-json output/summary.json \
  --log-file output/app.log
```

### Docker Hub

The GitHub Actions workflow publishes the image to Docker Hub when a commit reaches
`main` or when a version tag such as `v1.0.0` is pushed. Configure these repository
secrets in **Settings > Secrets and variables > Actions** before pushing:

- `DOCKERHUB_USERNAME`: your Docker Hub username
- `DOCKERHUB_TOKEN`: a Docker Hub access token with permission to push images

Create a Docker Hub repository named `data-processing-app`, then add the secrets and
push to GitHub. The workflow publishes these tags:

```text
docker.io/<your-username>/data-processing-app:latest
docker.io/<your-username>/data-processing-app:v1.0.0
docker.io/<your-username>/data-processing-app:sha-<commit>
```

To publish manually from a local machine:

```bash
docker login
docker build -t <your-username>/data-processing-app:latest .
docker push <your-username>/data-processing-app:latest
```

Pull and run the published image with:

```bash
docker pull <your-username>/data-processing-app:latest
docker run --rm <your-username>/data-processing-app:latest --help
```

## Data Format

The application expects CSV files with the following structure:

```
id,name,value
1,Alice,10.5
2,Bob,20.3
3,Charlie,15.8
```

## Processing Pipeline

1. **Load**: Read CSV file with chunking for memory efficiency
2. **Validate**: Check data quality (non-empty, has columns)
3. **Clean**: Remove duplicates and missing values
4. **Save**: Write processed data to output file

## Logging

The application provides detailed logging output. Log level can be configured via the `LOG_LEVEL` environment variable:

- `DEBUG`: Detailed information for debugging
- `INFO`: Confirmation that things are working as expected
- `WARNING`: Something unexpected happened
- `ERROR`: A serious problem occurred

## Error Handling

The application includes error handling for:

- Missing input files
- Invalid data formats
- File I/O errors
- Data validation failures

## Development

### Adding new features:

1. Add functionality to the appropriate module in `src/`
2. Write corresponding tests in `tests/`
3. Run tests to ensure everything works
4. Update this README if needed

### Code style:

- Follow PEP 8 conventions
- Use type hints where applicable
- Write docstrings for all functions
- Keep functions focused and modular

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **python-dotenv**: Environment variable management
- **pytest**: Testing framework

## License

This project is provided as-is for educational and development purposes.
