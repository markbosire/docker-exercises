# Docker Custom Networks Exercise

## Setup

Create a simple container with network tools:

**Dockerfile:**
```dockerfile
FROM alpine:latest
RUN apk add --no-cache curl iputils
CMD ["tail", "-f", "/dev/null"]
```

## Build the Image
```bash
docker build -t nettest .
```

## Exercise: Network Connectivity Test

### 1. Create Custom Network
```bash
# Create custom network
docker network create my-network
```

### 2. Run Three Containers
```bash
# Container A: On custom network
docker run -d --name container-a --network my-network nettest

# Container B: On custom network  
docker run -d --name container-b --network my-network nettest

# Container C: On default network (isolated)
docker run -d --name container-c nettest
```

### 3. Test Connectivity
```bash
# From container-a, ping container-b (should work - same network)
docker exec container-a ping -c 3 container-b

# From container-a, ping container-c (should fail - different networks)
docker exec container-a ping -c 3 container-c

# Check networks
docker network ls
docker network inspect my-network
```

### 4. Expected Results
- ✅ `container-a` can ping `container-b` (both on `my-network`)
- ❌ `container-a` cannot ping `container-c` (different networks)
- ❌ `container-c` cannot ping `container-a` or `container-b`

### 5. Connect Container C to Custom Network
```bash
# Connect container-c to custom network
docker network connect my-network container-c

# Now test again (should work)
docker exec container-a ping -c 3 container-c
```

## Cleanup
```bash
docker rm -f container-a container-b container-c
docker network rm my-network
```

## Key Commands
```bash
# List networks
docker network ls

# Create network
docker network create <network-name>

# Connect container to network
docker network connect <network-name> <container-name>

# Inspect network
docker network inspect <network-name>

# Remove network
docker network rm <network-name>
```

## Purpose
This exercise demonstrates Docker network isolation by showing how containers on the same custom network can communicate by name, while containers on different networks cannot reach each other, illustrating basic Docker networking concepts.
