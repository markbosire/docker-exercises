# Docker Bind Mounts vs Volumes

## Setup
```bash
# Pull Alpine image
docker pull alpine:latest

```

## Part 1: Bind Mounts

### Create a bind mount
```bash
# Create local file
echo "Hello from host" > host-file.txt

# Run container with bind mount
docker run -it --rm \
  -v $(pwd):/app \
  alpine:latest sh

# Inside container:
cd /app
ls                    # See host-file.txt
echo "Modified by container" >> host-file.txt
exit
```

### Verify changes persist on host
```bash
cat host-file.txt     # Shows both lines
```

## Part 2: Docker Volumes

### Create and use a volume
```bash
# Create named volume
docker volume create my-volume

# Run container with volume
docker run -it --rm \
  -v my-volume:/data \
  alpine:latest sh

# Inside container:
cd /data
echo "Hello from volume" > volume-file.txt
exit
```

### Access volume from another container
```bash
docker run -it --rm \
  -v my-volume:/data \
  alpine:latest sh

# Inside container:
cd /data
cat volume-file.txt   # Shows content from previous container
exit
```

## Part 3: Side-by-Side Comparison

### Test performance (bind mount)
```bash
docker run --rm \
  -v $(pwd):/app \
  alpine:latest \
  time dd if=/dev/zero of=/app/test-bind bs=1M count=100
```

### Test performance (volume)
```bash
docker run --rm \
  -v my-volume:/data \
  alpine:latest \
  time dd if=/dev/zero of=/data/test-volume bs=1M count=100
```

## Cleanup
```bash
# Remove volume
docker volume rm my-volume

# Remove test files
rm -f host-file.txt test-bind
```

## Summary

| Feature | Bind Mounts | Volumes |
|---------|-------------|---------|
| **Location** | Host filesystem path | Docker-managed |
| **Performance** | Slower (especially macOS/Windows) | Faster |
| **Portability** | Host-dependent paths | Portable across environments |
| **Backup** | Manual host backup | `docker volume` commands |
| **Security** | Host filesystem access | Isolated |
| **Use Case** | Development, config files | Production data, databases |

## When to Use

**Bind Mounts:**
- Development environments
- Configuration files
- Source code mounting
- Need direct host access

**Volumes:**
- Production databases
- Application data
- Sharing between containers
- Better performance needed