# Filename: Dockerfile
# Author: Szymon Manduk
# Company: Szymon Manduk AI, manduk.ai
# Description: Dockerfile for the search-notes application.
# Copyright (c) 2024 Szymon Manduk AI.
#
# To build this image: docker build -t search-notes:search-notes-latest .
# To test local API run this command from search-index directory:
# docker run -p 8000:8000 -e APP_MODE=api-mode-local --env-file ../.env search-notes:search-notes-latest
# Note: APP_MODE=api-mode-local is the default value, you can omit it. Uvicorn will be used.
# 
# To test Azure API run this command from search-index directory:
# docker run -p 8000:8000 -e APP_MODE=api-mode-azure --env-file ../.env search-notes:search-notes-latest
# Note: Gunicorn will be used.

# Use the official Python 3.11 image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Set an environment variable with a default value
# This value can be overridden when running the container: docker run -e APP_MODE=api-mode-azure your-image-name
ENV APP_MODE=api-mode-local

# Use CMD to run the application with the mode specified by APP_MODE
CMD python search_notes.py --mode $APP_MODE