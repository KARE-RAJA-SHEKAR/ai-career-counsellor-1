# Use a base image with Python
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the project
COPY . .

# Train Rasa model (optional if you already have one in models/)
RUN rasa train

# Expose necessary ports
EXPOSE 5005 8501

# Run both Rasa and Streamlit using a simple script
CMD ["sh", "-c", "rasa run --enable-api --cors \"*\" & streamlit run app.py --server.port=8501"]
