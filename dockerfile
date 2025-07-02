# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    # Add any other system dependencies needed by your Python packages here
    # e.g., libffi-dev for cryptography if not covered by build-essential
    && rm -rf /var/lib/apt/lists/* 
    # Clean up apt cache to keep image small
RUN pip install --upgrade pip
RUN pip install -r requirements.txt -v --no-cache-dir

# Copy project files
COPY . /app/

# Expose the port your app runs on
EXPOSE 5000

# Run the application with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "webhook_server:app"]