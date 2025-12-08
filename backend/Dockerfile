# Pull base image
FROM python:3.11.5-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install PostgreSQL client (for pg_isready)
RUN apt-get update && apt-get install -y postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . .

# Copy entrypoint script separately 
COPY entrypoint.sh /code/entrypoint.sh

# Make entrypoint executable inside the container
RUN chmod +x /code/entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/code/entrypoint.sh"]

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



