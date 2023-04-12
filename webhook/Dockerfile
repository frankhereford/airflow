# Base image
FROM python:3.9-slim-buster


# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /app

# Expose the port the app will run on
EXPOSE 5000

# Start the Flask app
CMD ["python", "webhook.py"]
