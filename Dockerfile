# syntax=docker/dockerfile:1
# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app


COPY requirements.txt requirements.txt


RUN pip install -r requirements.txt

COPY . .

# Install dependencies using Poetry, including Gunicorn
RUN poetry install --no-dev --no-interaction --no-ansi

# Add Poetry and Python binaries to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Expose the port Gunicorn will run on
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=plexplaylistmanager/__init__.py
ENV FLASK_ENV=production

# Start the application using Gunicorn, assuming the Flask app is named `app`
# and is located in the `__init__.py` file of your `plexplaylistmanager` package
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "plexplaylistmanager:app"]