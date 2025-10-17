# ----------------------------------------------------------------------
# STAGE 1: BUILD ENVIRONMENT
# Used to install system dependencies required for building Python packages
# (e.g., psycopg2, Pillow)
# ----------------------------------------------------------------------
FROM python:3.11-slim AS builder

# Set environment variables for non-interactive install and clean up
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install *build-time* system dependencies
# DEBIAN_FRONTEND=noninteractive is set to prevent interactive prompts
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libpq-dev \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        gettext \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install pip dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# ----------------------------------------------------------------------
# STAGE 2: FINAL PRODUCTION ENVIRONMENT
# Uses a minimal base image and copies only the necessary runtime files.
# ----------------------------------------------------------------------
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Create non-root user
ARG USER=app
ARG UID=1000
RUN groupadd -r $USER && useradd -r -g $USER -u $UID -m $USER

# Install *runtime* system dependencies (needed after build)
# Only libpq-dev is installed here, but its runtime dependency, libpq5, is needed.
# Additionally, libjpeg62-turbo is needed for Pillow runtime.
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libpq5 \
        libjpeg62-turbo \
        gettext \
        ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy installed Python packages from the builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy project code and entrypoint
COPY . /app
COPY deploy/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Ensure non-root user owns app
RUN chown -R $USER:$USER /app

# Switch to non-root user
USER $USER

# Environment variables
ENV DJANGO_SETTINGS_MODULE=your_project_name.settings

# Expose Django port
EXPOSE 9000

# Use entrypoint to run server
ENTRYPOINT ["/app/entrypoint.sh"]