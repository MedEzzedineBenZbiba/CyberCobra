FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for MySQL, face_recognition, etc.
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    default-libmysqlclient-dev \
    pkg-config \
    cmake \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Start application
CMD ["sh", "-c", "python manage.py migrate && gunicorn CyberCobra.wsgi:application --bind 0.0.0.0:$PORT --workers 3"]