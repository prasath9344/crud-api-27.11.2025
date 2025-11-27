# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first for efficient caching
COPY requirements.txt .

# Install Python dependencies (no cache for smaller image)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Default command to run your Python app
CMD ["python", "app.py"]
    