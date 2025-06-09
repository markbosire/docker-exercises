# Docker Exercise: Remove Containers and Clean Up

This exercise covers Docker cleanup operations to free up system resources.

## Prerequisites
- Docker installed and running

## Steps

### Create Test Containers
```bash
docker run -d --name cleanup-test1 nginx:alpine
docker run -d --name cleanup-test2 nginx:alpine
docker run -d --name cleanup-test3 nginx:alpine
```

### Stop Containers
```bash
docker stop cleanup-test1 cleanup-test2 cleanup-test3
```

### Remove Individual Container
```bash
docker rm cleanup-test1
```

### Remove Multiple Containers
```bash
docker rm cleanup-test2 cleanup-test3
```

### Force Remove Running Container
```bash
# Start a new container
docker run -d --name force-remove-test nginx:alpine

# Force remove without stopping
docker rm -f force-remove-test
```

### Bulk Cleanup Operations
```bash
# Create some containers to clean up
docker run -d --name temp1 nginx:alpine
docker run -d --name temp2 nginx:alpine
docker stop temp1 temp2

# Remove all stopped containers
docker container prune -f

# Remove unused images
docker image prune -f

# Remove unused networks
docker network prune -f

# Remove unused volumes
docker volume prune -f

# Remove everything unused (containers, networks, images, cache)
docker system prune -a -f
```

### Verify Cleanup
```bash
docker ps -a
docker images
docker network ls
docker volume ls
```

## What You Learned
- How to stop and remove containers individually
- How to force remove running containers
- How to use bulk cleanup commands
- How to verify system cleanup