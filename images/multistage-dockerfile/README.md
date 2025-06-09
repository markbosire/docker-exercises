# Docker Exercise: Multi-Stage Builds

This exercise demonstrates creating optimized Docker images using multi-stage builds with a Go application.

## Prerequisites
- Docker installed and running

## Steps

### Create Project Directory
```bash
mkdir go-multistage-demo
cd go-multistage-demo
```

### Create main.go
```bash
cat > main.go << 'EOF'
package main

import (
    "fmt"
    "net/http"
)

func main() {
    http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "Hello from Go multi-stage build!")
    })
    
    fmt.Println("Server starting on :8080")
    http.ListenAndServe(":8080", nil)
}
EOF
```

### Initialize Go Module
```bash
go mod init go-multistage-demo
```

### Create Multi-Stage Dockerfile
```bash
cat > Dockerfile << 'EOF'
# Stage 1: Build
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Stage 2: Production
FROM alpine:latest
RUN apk --no-cache add ca-certificates
WORKDIR /root/
COPY --from=builder /app/main .
EXPOSE 8080
CMD ["./main"]
EOF
```

### Build the Multi-Stage Image
```bash
docker build -t go-multistage-demo .
```

### Check Image Size
```bash
docker images go-multistage-demo
```

### Create Single-Stage Dockerfile for Comparison
```bash
cat > Dockerfile.single << 'EOF'
FROM golang:1.21-alpine
WORKDIR /app
COPY . .
RUN go mod download
RUN go build -o main .
EXPOSE 8080
CMD ["./main"]
EOF
```

### Build Single-Stage Image
```bash
docker build -f Dockerfile.single -t go-single-stage .
```

### Compare Image Sizes
```bash
docker images | grep go-
```

### Run the Multi-Stage Container
```bash
docker run -d -p 8080:8080 --name go-app go-multistage-demo
```

### Test the Application
```bash
curl http://localhost:8080
```

### Clean Up
```bash
docker stop go-app
docker rm go-app
docker rmi go-multistage-demo go-single-stage
cd ..
rm -rf go-multistage-demo
```

## What You Learned
- How to create multi-stage Dockerfiles
- How to copy artifacts between build stages
- How multi-stage builds reduce final image size
- The difference between build and production images