# Docker Container Networking Tutorial

## Overview
We'll create a simple web application that connects to a Redis database using Docker's user-defined networks.

## Step 1: Create Project Files

Create a new directory and add these files:

**app.py**
```python
from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)
redis_client = redis.Redis(host='redis-db', port=6379, decode_responses=True)

@app.route('/')
def home():
    try:
        count = redis_client.incr('visits')
        return jsonify({
            'message': f'Hello! You are visitor #{count}',
            'redis_host': 'redis-db'
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Dockerfile**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app.py .
RUN pip install flask redis
EXPOSE 5000
CMD ["python", "app.py"]
```

## Step 2: Create User-Defined Network

```bash
# Create a custom bridge network
docker network create myapp-network

# List networks to verify
docker network ls
```

## Step 3: Start Redis Container

```bash
# Run Redis container on our custom network
docker run -d \
  --name redis-container \
  --network myapp-network \
  --network-alias redis-db \
  redis:alpine

# Verify container is running
docker ps
```

## Step 4: Build and Run Web App

```bash
# Build the web app image
docker build -t myapp .

# Run web app container on the same network
docker run -d \
  --name web-container \
  --network myapp-network \
  -p 8080:5000 \
  myapp
```

## Step 5: Test the Connection

```bash
# Test the application
curl http://localhost:8080

# Should return: {"message": "Hello! You are visitor #1", "redis_host": "redis-db"}
```


## Cleanup

```bash
# Stop and remove containers
docker stop web-container redis-container 
docker rm web-container redis-container 
# Remove networks
docker network rm myapp-network 
```

## Summary

User-defined networks provide:
- **Automatic DNS resolution** between containers
- **Network isolation** for security
- **Easy container communication** using names instead of IPs
- **Multiple network connectivity** for complex architectures

The key advantage over default bridge networking is built-in service discovery and isolation.