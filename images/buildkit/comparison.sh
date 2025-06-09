#!/bin/bash

# Create temporary directory
tmpdir=$(mktemp -d)
cd "$tmpdir" || exit

# Create heavier Dockerfile
cat > Dockerfile <<EOF
FROM ubuntu:22.04

# Install multiple packages to make build heavier
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    python3 \
    python3-pip \
    nodejs \
    npm \
    openjdk-17-jdk \
    ruby-full \
    golang-go

# Create multiple files and directories
RUN mkdir /app && cd /app && \
    for i in {1..100}; do touch file_\$i.txt; done

# Run multiple commands to simulate complex build
RUN echo "Building application..." && \
    npm install -g create-react-app && \
    pip3 install pandas numpy scipy && \
    gem install rails && \
    go get github.com/gorilla/mux

# Add large build context
COPY . /build-context

# Final setup
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    echo "Build complete"
EOF

# Create large build context (10MB of random data)
mkdir -p context
dd if=/dev/urandom of=context/largefile.bin bs=1M count=10 status=none
for i in {1..50}; do
    echo "Build context file $i" > "context/file_$i.txt"
done

# Function to time builds
time_build() {
    local mode=$1
    local start end duration
    
    start=$(date +%s.%N)
    if [ "$mode" = "buildkit" ]; then
        DOCKER_BUILDKIT=1 docker build -q -t test-$mode . >/dev/null
    else
        DOCKER_BUILDKIT=0 docker build -q -t test-$mode . >/dev/null
    fi
    end=$(date +%s.%N)
    
    duration=$(echo "$end - $start" | bc -l)
    echo "$mode build time: ${duration}s"
}

# Run builds in parallel
echo "Starting parallel builds (this may take a while)..."
time_build buildkit &
time_build regular &

# Wait for both background jobs to finish
wait

# Cleanup
cd - >/dev/null
rm -rf "$tmpdir"
docker rmi test-buildkit test-regular >/dev/null 2>&1
