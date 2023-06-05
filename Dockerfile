# Base image
FROM python:3.10.6

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql postgresql-contrib && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files to the container
COPY poetry.lock pyproject.toml /app/

# Install dependencies
RUN pip install poetry==1.5.0
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app/

# Expose the port on which the application will run
EXPOSE 8000

# Initialize and migrate the database
RUN service postgresql start && \
    su - postgres -c "psql -c 'CREATE DATABASE aspex1_db;'" && \
    su - postgres -c "psql -c 'CREATE USER aspex1_user WITH ENCRYPTED PASSWORD '\''qwerty'\'';'" && \
    su - postgres -c "psql -c 'GRANT ALL PRIVILEGES ON DATABASE aspex1_db TO aspex1_user;'"

# todo: do we need it?
# RUN python -m alembic upgrade head

# Run the FastAPI application
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
