# Use the official Python image with version 3.12 as base
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy only the poetry-related files to leverage Docker cache
COPY poetry.lock pyproject.toml ./

# Install Poetry
RUN pip install --no-cache-dir poetry

# Install dependencies
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY . .

# Expose port for uvicorn
EXPOSE 8000

# Set environment variables
ENV OPENAI_API_KEY=""
ENV PASSWORD=""

# Run the application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
