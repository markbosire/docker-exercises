# Docker Exercise: Build Custom Images

This exercise covers building Docker images from Dockerfiles with various options and configurations.

## Prerequisites
- Docker installed and running

## Steps

### Create Simple Web App
```bash
mkdir custom-web-app
cd custom-web-app
```

### Create Application Files
```bash
# Create HTML file
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Custom Docker App</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Hello from Custom Docker Image!</h1>
    <p>Built with custom Dockerfile</p>
    <p>Version: 1.0</p>
</body>
</html>
EOF

# Create nginx config
cat > nginx.conf << 'EOF'
server {
    listen 80;
    server_name localhost;
    
    location / {
        root /usr/share/nginx/html;
        index index.html;
    }
}
EOF
```

### Create Basic Dockerfile
```bash
cat > Dockerfile << 'EOF'
FROM nginx:alpine
COPY index.html /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF
```

### Build Basic Image
```bash
docker build -t custom-web-app:v1 .
```

### Build with Latest Tag
```bash
docker build -t custom-web-app:latest .
```

### Create Dockerfile with Build Arguments
```bash
cat > Dockerfile.args << 'EOF'
FROM nginx:alpine
ARG APP_NAME=default-app
ARG VERSION=1.0.0
LABEL app.name=${APP_NAME}
LABEL app.version=${VERSION}
RUN echo "Building ${APP_NAME} version ${VERSION}"
COPY index.html /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
EOF
```

### Build with Custom Arguments
```bash
docker build -f Dockerfile.args --build-arg APP_NAME=my-web-app --build-arg VERSION=2.0.0 -t custom-web-app:v2 .
```

### Build from Different Directory
```bash
# Create another directory
mkdir ../another-app
cp index.html ../another-app/
cp Dockerfile ../another-app/

# Build from parent directory
docker build -f another-app/Dockerfile -t another-web-app ../another-app/
```

### View Built Images
```bash
docker images custom-web-app
docker images another-web-app
```

### Inspect Image Details
```bash
docker inspect custom-web-app:v2
```

### Test the Images
```bash
# Test v1
docker run -d -p 8080:80 --name web-test-v1 custom-web-app:v1
curl http://localhost:8080

# Test v2
docker run -d -p 8081:80 --name web-test-v2 custom-web-app:v2
curl http://localhost:8081

# Stop containers
docker stop web-test-v1 web-test-v2
docker rm web-test-v1 web-test-v2
```

### Clean Up
```bash
docker rmi custom-web-app:v1 custom-web-app:v2 custom-web-app:latest another-web-app
cd ..
rm -rf custom-web-app another-app
```

## What You Learned
- How to build images from Dockerfiles
- How to use different tags and naming conventions
- How to use build arguments for customization
- How to build from different directories and Dockerfiles
- How to inspect and test built images