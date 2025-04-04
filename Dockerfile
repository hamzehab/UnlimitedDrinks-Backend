# --- Build stage: extract requirements from Poetry ---
FROM python:3.11.4-slim-bookworm as build-stage

WORKDIR /tmp

# Install Poetry and the export plugin
RUN pip install --no-cache-dir poetry \
    && poetry self add poetry-plugin-export

# Copy dependency files
COPY pyproject.toml /tmp/
COPY poetry.lock /tmp/

# Export dependencies to requirements.txt
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


# --- Production stage: install dependencies and run the app ---
FROM python:3.11.4-slim-bookworm as prod-stage

# Install system dependencies for asyncpg and build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc g++ curl procps net-tools tini \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set environment variables
ENV PYTHONFAULTHANDLER=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY --from=build-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application
COPY . /app/

# Expose port
EXPOSE 5000

# Default command (adjust if needed)
CMD ["python", "main.py"]
