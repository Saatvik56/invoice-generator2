# Use the official lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright + Chromium
RUN playwright install --with-deps chromium

# Expose the port Railway assigns
EXPOSE 8000

# Run Gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
