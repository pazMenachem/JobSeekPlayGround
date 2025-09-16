# Simple but improved Dockerfile for calculatorCICD
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies first (for better caching)
COPY pyproject.toml .
COPY src/__init__.py src/
RUN pip install .

# Copy the rest of the source code
COPY src/ ./src/

# Run the calculator
CMD ["python", "-m", "src"]