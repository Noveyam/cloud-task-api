# Build stage-----------------
FROM python:3.12-slim AS builder

#Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .

#Build wheels
RUN pip install --upgrade pip && \
    mkdir -p /wheels && \
    pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# Runtime stage------------------
FROM python:3.12-slim AS runtime

#Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser

#Install from build stage
COPY --from=builder /wheels /wheels
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && \
    rm -rf /wheels

# Copy the rest of the app
COPY . .

# Switch to non-root user
USER appuser

# Expose app (Uvicorn)
EXPOSE 8000

#Run Uvicorn for Django ASGI app
CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]