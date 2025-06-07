# Docker Exercise: Tag and Push Images

This exercise covers tagging Docker images and pushing them to registries.

## Prerequisites
- Docker installed and running
- Docker Hub account (for public registry)

## Steps

### Create Sample Image
```bash
mkdir simple-app
cd simple-app

cat > Dockerfile << 'EOF'
FROM alpine:latest
RUN echo "Hello from Simple App v1.0" > /hello.txt
RUN echo "Built on $(date)" >> /hello.txt
CMD ["cat", "/hello.txt"]
EOF

docker build -t simple-app .
```

### Tag for Docker Hub
```bash
# Replace 'yourusername' with your actual Docker Hub username
docker tag simple-app:latest yourusername/simple-app:latest
docker tag simple-app:latest yourusername/simple-app:v1.0
docker tag simple-app:latest yourusername/simple-app:stable
```

### View Tagged Images
```bash
docker images yourusername/simple-app
```

### Login to Docker Hub
```bash
docker login
# Enter your Docker Hub username and password when prompted
```

### Push to Docker Hub
```bash
docker push yourusername/simple-app:latest
docker push yourusername/simple-app:v1.0
docker push yourusername/simple-app:stable
```

### Set Up Local Registry
```bash
# Start local registry
docker run -d -p 5000:5000 --name local-registry registry:2
```

### Tag for Local Registry
```bash
docker tag simple-app:latest localhost:5000/simple-app:latest
docker tag simple-app:latest localhost:5000/simple-app:v1.0
```

### Push to Local Registry
```bash
docker push localhost:5000/simple-app:latest
docker push localhost:5000/simple-app:v1.0
```

### Verify Registry Contents
```bash
# List repositories in local registry
curl http://localhost:5000/v2/_catalog

# List tags for specific repository
curl http://localhost:5000/v2/simple-app/tags/list
```

### Test Pull and Run
```bash
# Remove local images
docker rmi simple-app:latest
docker rmi localhost:5000/simple-app:latest

# Pull from local registry
docker pull localhost:5000/simple-app:latest

# Test the pulled image
docker run --rm localhost:5000/simple-app:latest
```

### Tag with Multiple Versions
```bash
# Create new version
cat > Dockerfile.v2 << 'EOF'
FROM alpine:latest
RUN echo "Hello from Simple App v2.0" > /hello.txt
RUN echo "Built on $(date)" >> /hello.txt
RUN echo "New feature added!" >> /hello.txt
CMD ["cat", "/hello.txt"]
EOF

# Build new version
docker build -f Dockerfile.v2 -t simple-app:v2.0 .

# Tag for registries
docker tag simple-app:v2.0 yourusername/simple-app:v2.0
docker tag simple-app:v2.0 localhost:5000/simple-app:v2.0

# Push both versions
docker push yourusername/simple-app:v2.0
docker push localhost:5000/simple-app:v2.0
```

### Clean Up
```bash
# Stop and remove local registry
docker stop local-registry
docker rm local-registry

# Remove local images
docker rmi simple-app:latest simple-app:v2.0
docker rmi yourusername/simple-app:latest yourusername/simple-app:v1.0 yourusername/simple-app:v2.0 yourusername/simple-app:stable
docker rmi localhost:5000/simple-app:latest localhost:5000/simple-app:v1.0 localhost:5000/simple-app:v2.0

# Clean up files
cd ..
rm -rf simple-app
```

## What You Learned
- How to tag images for different registries
- How to push images to Docker Hub
- How to set up and use a local registry
- How to manage multiple image versions
- How to verify registry contents and pull images