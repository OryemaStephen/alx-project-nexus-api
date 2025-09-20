# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y procps build-essential libpq-dev curl git && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (leverage caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir flake8

# Copy project files
COPY . .

# Copy and set entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose Django port
EXPOSE 8000

# Entrypoint handles migrations & static collection
ENTRYPOINT ["/entrypoint.sh"]

# Default command (Django dev server, replace with gunicorn in prod)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
