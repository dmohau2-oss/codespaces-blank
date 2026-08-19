<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# Data Processing App - Project Guidelines

## Project Type
Python data processing application with ETL pipeline capabilities.

## Technology Stack
- Python 3.8+
- Pandas for data manipulation
- NumPy for numerical operations
- SQLite for data storage
- Pytest for testing

## Code Style
- Follow PEP 8 conventions
- Use type hints where applicable
- Document functions with docstrings
- Keep functions focused and modular

## Development Workflow
1. Create feature branches for new functionality
2. Write tests alongside implementation
3. Run tests before committing
4. Update documentation as needed

## Testing
All code changes should include corresponding unit tests in the `tests/` directory.

## Data Processing
- Input data should be validated before processing
- Output data should be saved in the `data/` directory
- Implement error handling for data quality issues
