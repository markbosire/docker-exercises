# Docker BuildKit Exercise

## Enable BuildKit

### Method 1: Environment Variable
```bash
export DOCKER_BUILDKIT=1
```

### Method 2: Docker Daemon Configuration
```json
{
  "features": {
    "buildkit": true
  }
}
```

### Method 3: Per-build
```bash
DOCKER_BUILDKIT=1 docker build .
```

## Create Test Files

**Dockerfile:**
```dockerfile
# syntax=docker/dockerfile:1.4
FROM ubuntu:20.04

# BuildKit-specific features
WORKDIR /app

# Parallel builds
RUN apt-get update
RUN apt-get install -y curl && \
    curl -o /tmp/file1.txt https://httpbin.org/json
RUN apt-get install -y wget && \
    wget -O /tmp/file2.txt https://httpbin.org/json

# Mount cache
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt \
    apt-get update && \
    apt-get install -y python3 python3-pip

# Secret mount
RUN --mount=type=secret,id=mypassword \
    echo "Using secret: $(cat /run/secrets/mypassword)"

# Bind mount
COPY requirements.txt .
RUN --mount=type=bind,source=.,target=/src \
    pip3 install -r /src/requirements.txt

# Multi-platform
COPY app.py .
CMD ["python3", "app.py"]
```

**requirements.txt:**
```
requests==2.28.1
flask==2.2.2
```

**app.py:**
```python
print("BuildKit demo app")
import platform
print(f"Platform: {platform.platform()}")
```

**secret.txt:**
```
my-secret-password
```

## Exercise Commands

### 1. Basic BuildKit Build
```bash
# Enable BuildKit
export DOCKER_BUILDKIT=1

# Build with BuildKit
docker build -t buildkit-demo .
```

### 2. Advanced BuildKit Features

**Cache Mounts:**
```bash
# Build with cache mounts (faster subsequent builds)
docker build --target production -t buildkit-cache .

# Check cache usage
docker system df
```

**Secret Mounts:**
```bash
# Build with secret
docker build --secret id=mypassword,src=./secret.txt -t buildkit-secret .
```

### 3. Multi-stage with BuildKit

**Dockerfile.multi:**
```dockerfile
# syntax=docker/dockerfile:1.4
FROM ubuntu:20.04 AS base
RUN apt-get update && apt-get install -y python3 python3-pip

FROM base AS development
RUN pip3 install pytest flask-testing
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY app.py .

FROM base AS production
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt
COPY app.py .
CMD ["python3", "app.py"]
```

```bash
# Build specific stage
docker build --target development -f Dockerfile.multi -t buildkit-dev .
docker build --target production -f Dockerfile.multi -t buildkit-prod .
```

### 4. BuildKit Debugging

**Check BuildKit status:**
```bash
docker version
docker buildx version
```

**Enable build output:**
```bash
# Progress output
docker build --progress=plain -t buildkit-debug .

# Build with timing
time docker build -t buildkit-timing .
```

### 5. Advanced BuildKit Examples

**Dockerfile.advanced:**
```dockerfile
# syntax=docker/dockerfile:1.4
FROM ubuntu:20.04

# Heredoc syntax (BuildKit feature)
RUN <<EOF
apt-get update
apt-get install -y \
    curl \
    wget \
    vim
apt-get clean
rm -rf /var/lib/apt/lists/*
EOF

# Copy with exclusions
COPY --exclude=*.log --exclude=node_modules . /app

# Mount tmpfs
RUN --mount=type=tmpfs,target=/tmp \
    echo "Using tmpfs mount" > /tmp/test.txt

WORKDIR /app
```

### 6. BuildKit with Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: production
    environment:
      - DOCKER_BUILDKIT=1
```

```bash
# Build with compose
DOCKER_BUILDKIT=1 docker-compose build
```

## Key Features Demonstrated

### 1. Parallel Builds
- Independent RUN commands execute in parallel
- Faster build times

### 2. Cache Mounts
- Persistent cache across builds
- Package manager caches preserved

### 3. Secret Mounts
- Secure secret handling
- Secrets not stored in image layers

### 4. Bind Mounts
- Access to build context without COPY
- Useful for large files

### 5. Multi-platform Support
```bash
# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t multiplatform-app .
```

## BuildKit vs Legacy Builder

| Feature | Legacy | BuildKit |
|---------|--------|----------|
| Parallel builds | No | Yes |
| Cache mounts | No | Yes |
| Secret mounts | No | Yes |
| Multi-platform | Limited | Full |
| Progress output | Basic | Rich |
| Heredoc syntax | No | Yes |

## Troubleshooting

**Check BuildKit status:**
```bash
docker info | grep -i buildkit
```

**Disable BuildKit:**
```bash
export DOCKER_BUILDKIT=0
```

**Clear BuildKit cache:**
```bash
docker builder prune
```

## Purpose
This exercise introduces Docker BuildKit, Docker's next-generation build system that provides advanced features like parallel builds, cache mounts, secret handling, and improved performance over the legacy builder.
