# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Copy wait-for-it script
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose Django port
EXPOSE 8000

# Start Django with Gunicorn (production-ready)
CMD sh -c "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn social_media_feed.wsgi:application --bind 0.0.0.0:8000 --workers 4"

