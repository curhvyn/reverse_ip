# Stage 1: Build stage
FROM python:3.9 AS builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production stage
FROM python:3.9-slim AS production

# Set the working directory in the container
WORKDIR /app

# Copy the installed dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/

# Copy the rest of the application code into the container
COPY . .

# Expose port 5001 to the outside world
EXPOSE 5001

# Run the Flask application
CMD ["python", "app.py"]
