# Docker Exercise: Exec into Running Containers

This exercise teaches you how to access and inspect running Docker containers.

## Prerequisites
- Docker installed and running

## Steps

### Step 1: Start a Container
```bash
docker run -d --name test-nginx nginx:alpine
```

### Step 2: List Running Containers
```bash
docker ps
```

### Step 3: Execute Interactive Shell
```bash
docker exec -it test-nginx /bin/sh
```

### Step 4: Inspect the Environment
Once inside the container, run these commands:
```bash
# View environment variables
env

# Check file system
ls -la

# View running processes
ps aux

# Check nginx configuration
cat /etc/nginx/nginx.conf

# View nginx logs
cat /var/log/nginx/access.log

# Exit the container
exit
```

### Step 5: Execute Single Commands
```bash
# Run commands without entering interactive mode
docker exec test-nginx whoami
docker exec test-nginx pwd
docker exec test-nginx ls -la /etc/nginx/
```

### Step 6: Clean Up
```bash
docker stop test-nginx
docker rm test-nginx
```

## What You Learned
- How to access running containers interactively
- How to inspect container environment and processes
- How to execute single commands in containers
- Basic container filesystem navigation