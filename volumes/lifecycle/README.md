# Docker Volume Lifecycle Management

## Purpose
Docker volumes provide persistent data storage that survives container restarts and deletions. Managing their lifecycle ensures efficient storage usage and proper data persistence.

## Core Commands

### 1. Create Volume
```bash
docker volume create my-volume
docker volume create --driver local --opt type=tmpfs my-temp-volume
```
**When to use:** Before running containers that need persistent storage or shared data between containers.

### 2. Inspect Volume
```bash
docker volume inspect my-volume
docker volume inspect my-volume --format '{{.Mountpoint}}'
```
**When to use:** To check volume details, location, driver settings, or troubleshoot storage issues.

### 3. List Volumes
```bash
docker volume ls
docker volume ls --filter dangling=true
```
**When to use:** To see all volumes or find unused volumes taking up space.

### 4. Prune Volumes
```bash
docker volume prune
docker volume prune --force
```
**When to use:** To clean up unused volumes and free disk space. Run regularly for maintenance.

## Typical Workflow

1. **Create** volume before container deployment
2. **Inspect** to verify configuration
3. **Monitor** with `ls` to track usage
4. **Prune** periodically to clean unused volumes

## Quick Examples

```bash
# Create and use volume
docker volume create db-data
docker run -v db-data:/var/lib/mysql mysql

# Check volume details
docker volume inspect db-data

# Clean unused volumes
docker volume prune -f
```

## Best Practices
- Name volumes descriptively
- Inspect before deleting important data
- Prune regularly but carefully
- Use labels for better organization