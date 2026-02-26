# Use a lightweight Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependency file and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the source code into the container
COPY src/ ./src/

# Set the command to execute the pipeline
CMD ["python", "src/main.py"]