# Docker Image Layers & Size Analysis Exercise

## Create Sample Dockerfile

**Dockerfile:**
```dockerfile
FROM ubuntu:20.04

# Layer 1: Update package lists
RUN apt-get update

# Layer 2: Install packages
RUN apt-get install -y \
    curl \
    wget \
    vim \
    git

# Layer 3: Create directories
RUN mkdir -p /app/data /app/logs

# Layer 4: Download large file
RUN curl -o /tmp/large-file.zip https://releases.ubuntu.com/20.04/ubuntu-20.04.6-desktop-amd64.iso || echo "Demo file"

# Layer 5: Add application
COPY app.js /app/
WORKDIR /app

# Layer 6: Install dependencies (simulated)
RUN echo "Installing dependencies..." && \
    dd if=/dev/zero of=/tmp/dummy-deps bs=1M count=50

# Layer 7: Cleanup (ineffective)
RUN rm /tmp/large-file.zip /tmp/dummy-deps

CMD ["node", "app.js"]
```

**app.js:**
```javascript
console.log('Application running...');
```

## Exercise Commands

### 1. Build the Image
```bash
docker build -t layer-demo .
```

### 2. Analyze with docker history
```bash
# Basic history
docker history layer-demo

# Human readable sizes
docker history layer-demo --human

# No truncation
docker history layer-demo --no-trunc

# Show only size and created by
docker history layer-demo --format "table {{.Size}}\t{{.CreatedBy}}"
```

### 3. Detailed Layer Analysis
```bash
# Show all layers with full commands
docker history layer-demo --no-trunc --format "table {{.ID}}\t{{.Size}}\t{{.CreatedBy}}"

# Find largest layers
docker history layer-demo --format "table {{.Size}}\t{{.CreatedBy}}" | sort -hr
```

### 4. Compare with Optimized Version

**Dockerfile.optimized:**
```dockerfile
FROM ubuntu:20.04

# Combine operations to reduce layers
RUN apt-get update && \
    apt-get install -y \
        curl \
        wget \
        vim \
        git && \
    mkdir -p /app/data /app/logs && \
    curl -o /tmp/large-file.zip https://releases.ubuntu.com/20.04/ubuntu-20.04.6-desktop-amd64.iso || echo "Demo file" && \
    echo "Installing dependencies..." && \
    dd if=/dev/zero of=/tmp/dummy-deps bs=1M count=50 && \
    rm /tmp/large-file.zip /tmp/dummy-deps && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY app.js /app/
WORKDIR /app
CMD ["node", "app.js"]
```

```bash
# Build optimized version
docker build -f Dockerfile.optimized -t layer-demo-optimized .

# Compare histories
docker history layer-demo
docker history layer-demo-optimized
```

### 5. Advanced Analysis Tools

**Using dive (install separately):**
```bash
# Install dive tool
wget https://github.com/wagoodman/dive/releases/download/v0.10.0/dive_0.10.0_linux_amd64.deb
sudo apt install ./dive_0.10.0_linux_amd64.deb

# Analyze with dive
dive layer-demo
```

**Using docker inspect:**
```bash
# Get detailed layer information
docker inspect layer-demo | jq '.[0].RootFS.Layers'

# Check image size
docker images layer-demo
docker images layer-demo-optimized
```

## Key Analysis Points

### Layer Information
- **Created**: When layer was created
- **Size**: Layer size (0 for metadata-only layers)
- **Command**: Command that created the layer
- **Layer ID**: Unique identifier

### Size Optimization Tips
- Combine RUN commands
- Clean up in same layer
- Use multi-stage builds
- Choose smaller base images
- Remove package caches

## Sample Output Analysis
```
IMAGE          CREATED         SIZE      CREATED BY
layer-demo     2 minutes ago   150MB     /bin/sh -c rm /tmp/large-file.zip...
<missing>      2 minutes ago   0B        COPY app.js /app/
<missing>      2 minutes ago   50MB      /bin/sh -c echo "Installing deps"...
<missing>      3 minutes ago   100MB     /bin/sh -c curl -o /tmp/large-file...
```

## Common Issues
- **Large intermediate files**: Not cleaned in same layer
- **Package caches**: Not removed after installation
- **Unnecessary layers**: Too many RUN commands
- **Missing .dockerignore**: Large build context

## Purpose
This exercise teaches how to analyze Docker image layers using `docker history` and other tools to understand image composition, identify size issues, and optimize Docker images for better performance and storage efficiency.
