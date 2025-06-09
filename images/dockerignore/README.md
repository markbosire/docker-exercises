# Docker .dockerignore Exercise

## Quick Setup

Create a sample project structure:
```
project/
├── src/
│   └── app.js
├── tests/
│   └── test.js
├── node_modules/
│   └── (many files)
├── .git/
│   └── (git files)
├── README.md
├── .dockerignore
└── Dockerfile
```

## Create Sample Files

**src/app.js:**
```javascript
console.log('Hello Docker!');
```

**tests/test.js:**
```javascript
// Test file
console.log('Running tests...');
```

**Dockerfile:**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN ls -la
CMD ["node", "src/app.js"]
```

## Exercise Steps

### 1. Build Without .dockerignore
```bash
docker build -t test-without-ignore .
```
Note the build time and files copied.

### 2. Create .dockerignore
```
node_modules
.git
.gitignore
README.md
tests/
*.log
.env
Dockerfile
.dockerignore
```

### 3. Build With .dockerignore
```bash
docker build -t test-with-ignore .
```

### 4. Compare Results
```bash
# Check build context size
docker history test-without-ignore
docker history test-with-ignore

# Verify files in containers
docker run --rm test-with-ignore ls -la
```

## Key Observations

- **Build Speed**: Smaller context = faster builds
- **Image Size**: Fewer unnecessary files
- **Security**: Sensitive files excluded
- **Cache Efficiency**: Better layer caching

## Common .dockerignore Patterns
```
# Dependencies
node_modules/
vendor/

# Development files
*.log
.env*
.git/
.vscode/

# Documentation
README.md
docs/

# Tests
tests/
**/*test*

# Build artifacts
dist/
build/

# OS files
.DS_Store
Thumbs.db
```

## Purpose
This exercise demonstrates how .dockerignore files optimize Docker builds by excluding unnecessary files from the build context, resulting in faster builds, smaller images, and better security.
