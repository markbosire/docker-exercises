# Docker Build Caching Exercise

## Understanding Cache Behavior

Docker caches layers to speed up subsequent builds. This exercise demonstrates caching mechanisms and optimization strategies.

## Create Test Application

**app.js:**
```javascript
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.json({ message: 'Hello Docker Cache!', version: '1.0.0' });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

**package.json:**
```json
{
  "name": "cache-demo",
  "version": "1.0.0",
  "main": "app.js",
  "dependencies": {
    "express": "^4.18.2"
  },
  "scripts": {
    "start": "node app.js"
  }
}
```

## Exercise 1: Poor Caching Strategy

**Dockerfile.bad:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Bad: Copy everything first
COPY . .

# This will run every time any file changes
RUN npm install

CMD ["npm", "start"]
```

## Exercise 2: Good Caching Strategy

**Dockerfile.good:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Good: Copy package files first
COPY package*.json ./

# Cache dependencies installation
RUN npm ci --only=production

# Copy application code last
COPY . .

CMD ["npm", "start"]
```

## Exercise 3: Advanced Caching

**Dockerfile.advanced:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Multi-stage for better caching
FROM node:18-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:18-alpine AS development
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM dependencies AS production
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
CMD ["npm", "start"]
```

## Testing Cache Behavior

### 1. Initial Build (Cold Cache)
```bash
# Build with poor caching
time docker build -f Dockerfile.bad -t cache-bad .

# Build with good caching
time docker build -f Dockerfile.good -t cache-good .
```

### 2. Modify Application Code
```javascript
// Change app.js version
res.json({ message: 'Hello Docker Cache!', version: '2.0.0' });
```

### 3. Rebuild and Compare
```bash
# Rebuild both versions
time docker build -f Dockerfile.bad -t cache-bad .
time docker build -f Dockerfile.good -t cache-good .
```

Note: The good version should be much faster on the second build.

### 4. Modify Dependencies
```json
// Add to package.json
"dependencies": {
    "express": "^4.18.2",
    "lodash": "^4.17.21"
}
```

```bash
# Rebuild - both should reinstall dependencies
time docker build -f Dockerfile.bad -t cache-bad .
time docker build -f Dockerfile.good -t cache-good .
```

## Cache Inspection Commands

### Check Build Cache
```bash
# Show build cache
docker system df

# Detailed cache info
docker buildx du

# Show image layers
docker history cache-good
```

### Force Cache Invalidation
```bash
# Disable cache
docker build --no-cache -t cache-disabled .

# Rebuild from specific stage
docker build --target dependencies -t cache-deps .
```

## Advanced Caching Techniques

### 1. Cache Mounts (BuildKit)
**Dockerfile.buildkit:**
```dockerfile
# syntax=docker/dockerfile:1.4
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

# Mount npm cache
RUN --mount=type=cache,target=/root/.npm \
    npm ci --only=production

COPY . .
CMD ["npm", "start"]
```

### 2. Multi-stage Cache Optimization
**Dockerfile.multistage:**
```dockerfile
FROM node:18-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS deps
RUN npm ci --only=production

FROM base AS build
RUN npm ci
COPY . .
RUN npm run build

FROM base AS runtime
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/dist ./dist
CMD ["node", "dist/app.js"]
```

### 3. Conditional Caching
**Dockerfile.conditional:**
```dockerfile
FROM node:18-alpine

WORKDIR /app

# Cache package installation
COPY package*.json ./
RUN npm ci --only=production

# Cache source code layers
COPY src/ ./src/
COPY public/ ./public/

# Config files that change less frequently
COPY config/ ./config/

# Main application file
COPY app.js ./

CMD ["npm", "start"]
```

## Cache Busting Strategies

### 1. Version-based Caching
```dockerfile
FROM node:18-alpine
WORKDIR /app

# Use version as cache key
ARG APP_VERSION=1.0.0
COPY package*.json ./
RUN npm ci --only=production

COPY . .
LABEL version=$APP_VERSION
CMD ["npm", "start"]
```

Build with version:
```bash
docker build --build-arg APP_VERSION=2.0.0 -t versioned-app .
```

### 2. Checksum-based Caching
```dockerfile
FROM node:18-alpine
WORKDIR /app

# Create checksum file
COPY package*.json ./
RUN npm ci --only=production

# Copy files with different change frequencies separately
COPY config/ ./config/
COPY src/ ./src/
COPY app.js ./

CMD ["npm", "start"]
```

## Monitoring Cache Effectiveness

### Build Time Comparison
```bash
#!/bin/bash
echo "=== First build (cold cache) ==="
time docker build -t cache-test .

echo "=== Second build (warm cache) ==="
time docker build -t cache-test .

echo "=== After code change ==="
# Modify app.js
sed -i 's/1.0.0/2.0.0/' app.js
time docker build -t cache-test .
```

### Cache Hit Rate Analysis
```bash
# Analyze cache usage
docker system events --filter type=image --filter event=build &
docker build -t cache-analysis .
```

## Best Practices Summary

1. **Copy dependencies first**: Package files before source code
2. **Order by change frequency**: Less frequently changed files first
3. **Use multi-stage builds**: Separate build and runtime dependencies
4. **Leverage BuildKit**: Cache mounts for package managers
5. **Avoid cache invalidation**: Careful with COPY and ADD commands
6. **Use .dockerignore**: Exclude unnecessary files from context

## Common Cache Pitfalls

- Copying entire project before dependencies
- Using `npm install` instead of `npm ci`
- Not using .dockerignore
- Frequent changes to early layers
- Large files invalidating cache

## Purpose
This exercise demonstrates Docker's layer caching mechanism and teaches strategies to optimize build times by understanding cache invalidation, proper layer ordering, and advanced caching techniques.
