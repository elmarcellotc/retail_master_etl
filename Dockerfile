# Use the official Python 3.13 image based on Windows Server Core LTSC 2025
FROM python:3.14

# Set the working directory inside the container
WORKDIR /app

ARG MYSQL_HOST
ARG MYSQL_ETL_USER
ARG MYSQL_ETL_PASSWORD
ARG MYSQL_PORT
ARG MYSQL_DATABASE

ENV MYSQL_HOST=${MYSQL_HOST}
ENV MYSQL_ETL_USER=${MYSQL_ETL_USER}
ENV MYSQL_ETL_PASSWORD=${MYSQL_ETL_PASSWORD}
ENV MYSQL_PORT=${MYSQL_PORT}
ENV MYSQL_DATABASE=${MYSQL_DATABASE}

# Copy requirements.txt first (for better layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
# Specifically: main.py, data_raw/, tests/, utils/
COPY main.py .
COPY data_raw ./data_raw/
COPY tests ./tests/
COPY utils ./utils/