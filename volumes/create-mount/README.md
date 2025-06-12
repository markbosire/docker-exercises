# Docker Volumes

## What are Docker Volumes?
Volumes persist data outside containers. Without volumes, data is lost when containers are removed.

## Step 1: Create a Named Volume
```bash
docker volume create mydata
```

## Step 2: Run Container with Volume
```bash
docker run -it --name container1 -v mydata:/data alpine sh
```

## Step 3: Create Data Inside Container
```bash
# Inside the container
echo "This data will persist!" > /data/important.txt
echo "Container 1 was here" >> /data/log.txt
exit
```

## Step 4: Remove the Container
```bash
docker rm container1
```

## Step 5: Create New Container with Same Volume
```bash
docker run -it --name container2 -v mydata:/data alpine sh
```

## Step 6: Verify Data Persistence
```bash
# Inside the new container
cat /data/important.txt  # Shows: This data will persist!
cat /data/log.txt        # Shows: Container 1 was here
echo "Container 2 was here too" >> /data/log.txt
exit
```

## Persistence Illustration

```
┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│ Container 1 │    │   mydata     │    │ Container 2 │
│             │◄──►│   Volume     │◄──►│             │
│ /data       │    │              │    │ /data       │
└─────────────┘    │ important.txt│    └─────────────┘
     ↓             │ log.txt      │         ↑
   Removed         │              │    Uses same data
                   └──────────────┘
```

## Clean Up
```bash
# Remove container
docker rm container2

# Remove volume
docker volume rm mydata
```

## Key Point
The volume exists independently of containers. Data survives container removal and can be shared between containers.