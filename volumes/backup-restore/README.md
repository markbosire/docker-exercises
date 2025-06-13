# Docker Volume Backup & Restore

## Purpose
Learn to backup and restore Docker volume data to prevent data loss and migrate containers between environments.

## When to Use
- **Backup**: Before system upgrades, container updates, or regular data protection
- **Restore**: After data corruption, system failures, or when migrating to new environments

## Exercises

### Exercise 1: Create Test Data

**Purpose**: Set up a container with data to practice backup/restore

```bash
# Create a named volume
docker volume create mydata

# Run container with volume and create test data
docker run -it --name testapp -v mydata:/data alpine sh

# Inside container, create test files
echo "Important data" > /data/important.txt
echo "Config settings" > /data/config.json
exit
```

### Exercise 2: Backup Volume Data

**Purpose**: Create a backup of volume data using tar

```bash
# Method 1: Backup to host directory
docker run --rm -v mydata:/data -v $(pwd):/backup alpine tar czf /backup/mydata-backup.tar.gz -C /data .

```

### Exercise 3: Restore Volume Data

**Purpose**: Restore data from backup to a new or existing volume

```bash
# Create new volume for restore
docker volume create mydata-restored

# Restore from backup
docker run --rm -v mydata-restored:/data -v $(pwd):/backup alpine tar xzf /backup/mydata-backup.tar.gz -C /data

# Verify restore
docker run --rm -v mydata-restored:/data alpine ls -la /data
```

### Exercise 4: Complete Backup Strategy

**Purpose**: Implement automated backup with timestamps

```bash
# Create timestamped backup
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker run --rm -v mydata:/data -v $(pwd):/backup alpine tar czf /backup/mydata-backup-$TIMESTAMP.tar.gz -C /data .

# List backups
ls -la *backup*.tar.gz
```

### Exercise 5: Database Backup Example

**Purpose**: Backup database data properly

```bash
# Run MySQL container
docker run -d --name mysql-db -v mysql-data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret mysql:8.0

# Backup database data
docker run --rm -v mysql-data:/data -v $(pwd):/backup alpine tar czf /backup/mysql-backup.tar.gz -C /data .

# Stop container before restore
docker stop mysql-db
docker rm mysql-db

# Restore to new volume
docker volume create mysql-data-restored
docker run --rm -v mysql-data-restored:/data -v $(pwd):/backup alpine tar xzf /backup/mysql-backup.tar.gz -C /data
```

## Key Commands Summary

```bash
# Backup
docker run --rm -v SOURCE_VOLUME:/data -v $(pwd):/backup alpine tar czf /backup/BACKUP_NAME.tar.gz -C /data .

# Restore
docker run --rm -v TARGET_VOLUME:/data -v $(pwd):/backup alpine tar xzf /backup/BACKUP_NAME.tar.gz -C /data

# List volumes
docker volume ls

# Inspect volume
docker volume inspect VOLUME_NAME
```

## Best Practices

1. **Stop containers** before backup for consistency
2. **Use timestamps** in backup filenames
3. **Test restores** regularly
4. **Store backups** in multiple locations
5. **Document** backup procedures

## Cleanup

```bash
# Remove test containers and volumes
docker rm testapp mysql-db
docker volume rm mydata mydata-restored mysql-data mysql-data-restored backup-storage
rm -f *.tar.gz
```
