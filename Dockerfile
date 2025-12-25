FROM python:3.13-slim
# Base image: official Python slim image (Debian-based) with Python 3.13 installed.

# Environment variables to ensure Python behaves well in Docker
ENV PYTHONDONTWRITEBYTECODE=1  \
PYTHONUNBUFFERED=1         
# disable output buffering (logs appear immediately)

# Set working directory inside the container to /app
WORKDIR /app

# Install system dependencies required to build Python packages and connect to Postgres
# - apt-get update: refresh package lists
# - apt-get install: install build-essential (compilers), libpq-dev (Postgres headers), gcc (C compiler)
# - --no-install-recommends: keep the image small by not installing recommended packages
# - rm -rf /var/lib/apt/lists/*: clean apt cache to reduce image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        gcc && \
    rm -rf /var/lib/apt/lists/*


# Copy requirements file and install Python dependencies
# COPY requirements.txt: copy only the requirements first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt
# Upgrade pip and install packages from requirements.txt
RUN pip install --upgrade pip && pip install -r /app/requirements.txt 

# Copy the rest of the application code into the container
# This includes manage.py, app packages, templates, static files, etc.
COPY . /app

# Create a non-root system user 'appuser' and make /app owned by that user
# Running as non-root inside containers is a recommended security practice


RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app \
    && chmod +x /app/entrypoint.sh

USER appuser


# Expose port 8000 (the port our Gunicorn server will bind to)
EXPOSE 8000

# Use an entrypoint script (entrypoint.sh) to run migrations and collectstatic on container start
ENTRYPOINT ["sh", "./entrypoint.sh"]

# Default command to run Gunicorn server
CMD ["gunicorn", "jobseeker.wsgi:application", "--bind", "0.0.0.0:8000"]

# The Dockerfile sets up a production-ready Django application container using Gunicorn as the WSGI server.
