# Use Playwright's official Python image (includes browsers)
FROM mcr.microsoft.com/playwright/python:latest

# Set working directory
WORKDIR /app

# Copy dependency file first for docker layer caching
COPY requirements.txt /app/requirements.txt

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY . /app

# Create a directory for temporary output (if your app writes PDFs)
RUN mkdir -p /app/output

# Expose a default port (helpful for local testing)
EXPOSE 8080

# Run using gunicorn and bind to Render's provided $PORT
CMD exec gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
