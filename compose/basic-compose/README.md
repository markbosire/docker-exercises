# Docker Compose Multi-Service

## Purpose
Docker Compose orchestrates multiple containers as a single application stack. Use it when your app needs multiple services (web server, database, cache) that must communicate together.

## When to Use Docker Compose
- **Multi-container applications** (web + database + redis)
- **Development environments** requiring consistent setup
- **Service communication** between containers
- **Volume and network management** across services

## Basic docker-compose.yml Structure

### Example: Python Connection Status App

```yaml
version: '3.8'

services:
  # Python Web App - Shows connection status
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis
    volumes:
      - .:/app

  # PostgreSQL Database
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=myapp
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data

  # Redis Cache
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

**Python App (app.py) - Connection Status Dashboard:**
```python
from flask import Flask, render_template_string
import psycopg2
import redis
import os

app = Flask(__name__)

@app.route('/')
def status():
    postgres_status = check_postgres()
    redis_status = check_redis()
    
    template = '''
    <h1>Service Connection Status</h1>
    <div style="font-size: 20px;">
        <p>PostgreSQL: {{ postgres_status }}</p>
        <p>Redis: {{ redis_status }}</p>
    </div>
    '''
    
    return render_template_string(template, 
                                postgres_status=postgres_status,
                                redis_status=redis_status)

def check_postgres():
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        conn.close()
        return "✅ Connected"
    except:
        return "❌ Not Connected"

def check_redis():
    try:
        r = redis.from_url(os.getenv('REDIS_URL'))
        r.ping()
        return "✅ Connected"
    except:
        return "❌ Not Connected"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Dockerfile for Python App:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

**requirements.txt:**
```
Flask==2.3.3
psycopg2-binary==2.9.7
redis==4.6.0
```

## Key Components Explained

### Services Section
- **web**: Your main application container
- **db**: Database service (PostgreSQL)
- **redis**: Caching/session storage

### Essential Configuration

**Ports**: Map container ports to host
```yaml
ports:
  - "host_port:container_port"
```

**Environment**: Set environment variables
```yaml
environment:
  - KEY=value
  - DATABASE_URL=connection_string
```

**Volumes**: Persist data and mount code
```yaml
volumes:
  - host_path:container_path
  - named_volume:container_path
```

**Depends_on**: Control startup order
```yaml
depends_on:
  - db
  - redis
```

## Step-by-Step Usage

### 1. Create docker-compose.yml
Place in your project root directory

### 2. Start All Services
```bash
docker compose up
```
*Builds images, creates networks, starts containers*

### 3. Run in Background
```bash
docker compose up -d
```
*Detached mode - runs services in background*

### 4. View Running Services
```bash
docker compose ps
```

### 5. View Logs
```bash
docker compose logs [service_name]
```

### 6. Stop Services
```bash
docker compose down
```
*Stops and removes containers, preserves volumes*

### 7. Rebuild and Start
```bash
docker compose up --build
```
*Rebuilds images before starting*

## Common Patterns

### Development Setup
```yaml
volumes:
  - .:/app  # Mount source code for live reload
environment:
  - NODE_ENV=development
```

### Production Setup
```yaml
restart: unless-stopped
environment:
  - NODE_ENV=production
```

### Health Checks
```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
```

## When to Use Each Step

- **Development**: Use `docker compose up` for active development
- **Testing**: Use `docker compose up -d` for background testing
- **Debugging**: Use `docker compose logs` to troubleshoot
- **Cleanup**: Use `docker compose down -v` to remove volumes
- **Production**: Consider Docker Swarm or Kubernetes instead

## Container Connection Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                Docker Compose Network                       │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   PYTHON    │    │ POSTGRESQL  │    │    REDIS    │     │
│  │   WEB APP   │    │ DATABASE    │    │   CACHE     │     │
│  │             │◄──►│             │    │             │     │
│  │ Shows:      │    │ Port 5432   │    │ Port 6379   │     │
│  │ ✅ DB OK    │    │ user/pass   │    │ Key-Value   │     │
│  │ ✅ Redis OK │◄───┼─────────────┼────┤ Storage     │     │
│  │ Port 5000   │    │             │    │             │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│         │                                                  │
│         ▼                                                  │
│    localhost:5000                                          │
└─────────────────────────────────────────────────────────────┘
```

**What the Python app shows:**
- Visit `localhost:5000` to see connection status
- Green ✅ when services are connected
- Red ❌ when services are down