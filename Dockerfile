# Lightweight Python image
FROM python:3.11-slim AS runtime

# Environment setup
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/home/user/.local/bin:$PATH"

# Install system deps (headless)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# --- FIX: Upgrade core tools as ROOT to patch vulnerabilities in /usr/local ---
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Create non-root user early
RUN useradd -m -u 1000 user

# Copy and install requirements
# We copy as root but install as user if we want, OR just install everything as root and use the user for running.
# Best practice is to install as root (system-wide) but RUN as user.
WORKDIR /app
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY --chown=user . .

# Set PYTHONPATH
ENV PYTHONPATH=/app

USER user
EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
