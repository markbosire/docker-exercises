# Docker Service Dependencies and Startup Order

## Purpose
Control when and how services start in Docker Compose to ensure proper application initialization and avoid connection failures between dependent services.

## Core Concepts

### 1. `depends_on` - Basic Dependency Control
Controls startup order but **doesn't wait for service readiness**.

```yaml
version: '3.8'
services:
  web:
    image: nginx
    depends_on:
      - db
  
  db:
    image: postgres:13
```

**Use when:** You need basic startup ordering but services can handle connection retries.

### 2. `depends_on` with Health Checks
Waits for services to be healthy before starting dependents.

```yaml
version: '3.8'
services:
  web:
    image: myapp
    depends_on:
      db:
        condition: service_healthy
  
  db:
    image: postgres:13
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

**Use when:** Services must be fully ready before dependents start.

### 3. Wait Scripts
Custom scripts that wait for specific conditions.

```yaml
version: '3.8'
services:
  web:
    image: myapp
    command: ["./wait-for-it.sh", "db:5432", "--", "npm", "start"]
    depends_on:
      - db
  
  db:
    image: postgres:13
```

**Use when:** You need custom readiness logic or working with external services.

## Step-by-Step Examples

### Example 1: Web App with Database
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      backend:
        condition: service_healthy
  
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
  
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: myapp
      POSTGRES_PASSWORD: password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```

### Example 2: Microservices with Message Queue
```yaml
version: '3.8'
services:
  api-gateway:
    image: nginx
    depends_on:
      - user-service
      - order-service
  
  user-service:
    build: ./user-service
    depends_on:
      redis:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
  
  order-service:
    build: ./order-service
    depends_on:
      postgres:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
  
  redis:
    image: redis:alpine
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
  
  postgres:
    image: postgres:13
    healthcheck:
      test: ["CMD-SHELL", "pg_isready"]
      interval: 10s
      timeout: 5s
      retries: 3
  
  rabbitmq:
    image: rabbitmq:3-management
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "ping"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## When to Use Each Method

| Method | Use Case | Pros | Cons |
|--------|----------|------|------|
| Basic `depends_on` | Simple apps with retry logic | Fast startup | No readiness check |
| Health check `depends_on` | Critical dependencies | Ensures readiness | Slower startup |
| Wait scripts | Complex conditions | Flexible | Requires custom scripts |

## Common Health Check Commands

### Database Services
```yaml
# PostgreSQL
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U $POSTGRES_USER"]

# MySQL
healthcheck:
  test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]

# MongoDB
healthcheck:
  test: ["CMD", "mongo", "--eval", "db.adminCommand('ping')"]
```

### Web Services
```yaml
# HTTP endpoint
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080/health"]

# TCP port
healthcheck:
  test: ["CMD-SHELL", "nc -z localhost 8080"]
```

## Best Practices

1. **Always use health checks** for critical dependencies
2. **Set appropriate timeouts** - balance startup speed with reliability
3. **Implement retry logic** in your application code
4. **Use init containers** for one-time setup tasks
5. **Monitor startup logs** to debug dependency issues

## Troubleshooting

```bash
# Check service health status
docker-compose ps

# View health check logs
docker inspect <container_name> | grep -A 10 Health

# Test health check manually
docker exec <container> <health_check_command>
```

