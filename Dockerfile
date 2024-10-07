# Use the official Python image from the Docker Hub
FROM python:3.12-slim

# Update the package list and install make and remove the package list (cached files created by apt-get update)
RUN apt-get update && apt-get install -yq make build-essential gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files from the current directory to the container ./
COPY pyproject.toml poetry.lock ./

# Install dependencies without installing the whole project
RUN poetry install --no-root

# Copy the rest of the application code from the host . to the container .
COPY . .

# Set environment variables
ENV FLASK_APP=main
ENV FLASK_RUN_HOST=0.0.0.0

# Expose the port the app runs on
# Render handles the port assignment

EXPOSE 1624

# Run the application
# Remove --port=$PORT since Render assigns the port dynamically
# If there is no need to handle a specific port, the port can be removed from the command
CMD ["poetry", "run", "gunicorn", "--bind=0.0.0.0:1624", "-t", "60", "main:app"]