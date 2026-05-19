FROM ghcr.io/benoitc/gunicorn:24

# Set up container
WORKDIR /backend
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
COPY requirements.txt /backend/
RUN pip install --no-cache-dir -r requirements.txt

# Set up server
COPY --chown=gunicorn:gunicorn . .
RUN python manage.py check --deploy

# Start server
CMD ["core.asgi:application", "--workers", "4", "--worker-class", "asgi"]
