FROM python:3.11-slim

# Prevent python from buffering stdout/stderr and writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

WORKDIR /opt/app-root/src

# Install system libraries needed by Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Run collectstatic for production static file serving
RUN python manage.py collectstatic --noinput

# Run migrations
RUN python manage.py migrate

# Grant permissions for arbitrary user IDs (standard Red Hat OpenShift security requirement)
RUN chgrp -R 0 /opt/app-root/src && \
    chmod -R g=u /opt/app-root/src

EXPOSE 8080

CMD ["gunicorn", "DFD.wsgi:application", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120"]
