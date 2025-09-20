# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables, use key=value to avoid legacy warnings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies in one RUN to leverage caching and reduce layers
RUN apt-get update && \
    apt-get install -y procps build-essential libpq-dev curl git && \
    rm -rf /var/lib/apt/lists/*

# Declare build argument for pip cache directory before RUN
ARG PIP_CACHE_DIR=/root/.cache/pip

# Upgrade pip and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --cache-dir $PIP_CACHE_DIR -r requirements.txt && \
    pip install --no-cache-dir flake8

# Copy project files after installing dependencies to maximize cache hits
COPY . .

# Copy entrypoint script to container and make it executable
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Use entrypoint to handle migrations and static collection at container start
ENTRYPOINT ["/entrypoint.sh"]

# Default command - replace with your app server like gunicorn if needed
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
