FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app directory
COPY app/ ./app/

# Expose the default Streamlit port
EXPOSE 8501

# Command to run the Streamlit application
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]