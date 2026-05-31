FROM python:3.10-slim

WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy full project
COPY . .

EXPOSE 8000

# Run Flask app via gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "--timeout", "300", "app.app:app"]
