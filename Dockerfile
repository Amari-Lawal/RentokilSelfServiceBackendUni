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

# Create non-root user early (reduces COPY layer overhead)
RUN useradd -m -u 1000 user
USER user

# Copy and install requirements
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=user . /home/user/blustorymicroservices/BluStoryAccounts/

# Set PYTHONPATH so Python can find the top-level package
ENV PYTHONPATH=/home/user
WORKDIR /home/user/blustorymicroservices/BluStoryAccounts

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
