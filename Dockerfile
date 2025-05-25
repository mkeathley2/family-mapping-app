# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py .
COPY templates/ templates/
COPY sample_addresses.csv .

# Create datasets directory with proper permissions
RUN mkdir -p datasets && chmod 755 datasets

# Expose port 8765
EXPOSE 8765

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run the application
CMD ["python", "-c", "import app; app.app.run(host='0.0.0.0', port=8765, debug=False)"] 