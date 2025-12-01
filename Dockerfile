# Use the specified Python version
FROM python:3.9.7-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# ENV C_FORCE_ROOT true 

# Install system dependencies required for database drivers (psycopg2) and compiling
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client \
    gcc \
    libpq-dev \
    # Clean up to keep the image size small
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*


# Set the working directory in the container
WORKDIR /app

RUN python3 -m venv venv
ENV VIRTUAL_ENV=/app/venv
ENV PATH="/app/venv/bin:$PATH"

#Your Dockerfile sets ENV PATH="/app/venv/bin:$PATH".

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project (assuming it's in the same directory as the Dockerfile)
COPY . /app/

COPY ./wait-for-db.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/wait-for-db.sh


#uvicorn app.main:app --reload  

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
