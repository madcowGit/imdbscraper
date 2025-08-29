# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port Flask runs on (default 10000, can be overridden by PORT env)
EXPOSE 10000

# Set environment variable for Python
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]