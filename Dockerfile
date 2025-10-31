# Use Debian-based Python image (non-slim) to avoid missing packages
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install system dependencies required for Chromium and fonts
RUN apt-get update && apt-get install -y \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libgbm1 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libxi6 \
    libxcursor1 \
    libgtk-3-0 \
    fonts-liberation \
    fonts-noto-color-emoji \
    fonts-noto \
    fonts-freefont-ttf \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright + Chromium
RUN pip install playwright && playwright install chromium

# Expose Railway port
EXPOSE 8000

# Start the app
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
