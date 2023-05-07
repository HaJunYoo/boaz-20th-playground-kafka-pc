FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# RUN pip install kafka-python

WORKDIR /app
COPY . /app

# Expose Kafka port
EXPOSE 9092

# CMD ["python", "consumer.py"]

RUN pip install kafka-python