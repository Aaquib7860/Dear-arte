FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app app

# Security: Ensure only .pkl files are present, no source code
# The app/services/secure/gcp_service.pkl should be built before Docker build
RUN if [ ! -f "app/services/secure/gcp_service.pkl" ]; then \
        echo "ERROR: Secure package not found. Run 'python scripts/build_secure_package.py' first"; \
        exit 1; \
    fi

# Remove original source files if they exist (extra security layer)
RUN find /app -name "*_original.py" -delete || true

# Set Python to not write .pyc files and unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
