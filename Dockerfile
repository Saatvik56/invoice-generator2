# Use Debian-based Python image (includes required libs for Playwright)
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy all project files into container
COPY . .

# Install system dependencies required for Playwright + Chromium + fonts
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
    # ✅ Font packages for bold/regular text
    fonts-liberation \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    fonts-freefont-ttf \
    fonts-noto \
    fonts-noto-color-emoji \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright + Chromium browser
RUN pip install playwright && playwright install chromium

# Expose port for Railway (it assigns a dynamic port)
EXPOSE 8000

# Start the app using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
