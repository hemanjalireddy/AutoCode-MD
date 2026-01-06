FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential curl

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install deps (no dev tools)
RUN poetry config virtualenvs.create false \
    && poetry config installer.max-workers 1 \
    && export POETRY_HTTP_TIMEOUT=1200 \
    && poetry install --no-root --without dev

# Copy the backend code
COPY src/backend ./src/backend

# Set Python path so it finds 'src'
ENV PYTHONPATH=/app

# Run the server
CMD ["uvicorn", "src.backend.main:app", "--host", "0.0.0.0", "--port", "8000"]