FROM python:3.12-slim

WORKDIR /app

# Install minimal runtime deps (none required for this simple project)
ENV PYTHONUNBUFFERED=1

# Copy project files
COPY . /app

# Use a non-root user for safety
RUN useradd --create-home appuser || true
USER appuser

# Default command runs the main script
CMD ["python", "main.py"]
