FROM python:3.14-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY app.py assistant.py ./
COPY assets/ ./assets/

# Streamlit configuration
EXPOSE 8501

# Run Streamlit in headless mode
CMD ["streamlit", "run", "app.py", "--server.headless", "true", "--server.port", "8501"]
