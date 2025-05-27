# Docker Container Lifecycle & Best Practices  

This guide explains the **Docker container lifecycle**, key commands, and **best practices** for efficient and secure container management.  

---

## 🚀 Docker Container Lifecycle  

A Docker container goes through several stages:  

1. **Create** → `docker create` *(creates but does not start)*  
2. **Start** → `docker start` *(stops and starts)*  
3. **Run** → `docker run` *(create + start in one command)*  
4. **Pause/Unpause** → `docker pause` / `docker unpause` *(freezes without stopping)*  
5. **Stop** → `docker stop` *(graceful shutdown)*  
6. **Kill** → `docker kill` *(forceful shutdown)*  
7. **Remove** → `docker rm` *(deletes container)*  

### 📌 Key Commands  

| Command | Description | Example |
|---------|-------------|---------|
| `docker create` | Creates a container without starting it | `docker create -p 8080:80 nginx` |
| `docker start` | Starts a stopped container | `docker start my-nginx` |
| `docker run` | Creates and starts a container | `docker run -d --name my-nginx -p 8080:80 nginx` |
| `docker pause` | Freezes a running container | `docker pause my-nginx` |
| `docker unpause` | Resumes a paused container | `docker unpause my-nginx` |
| `docker stop` | Stops a running container (SIGTERM) | `docker stop my-nginx` |
| `docker kill` | Force-stops a container (SIGKILL) | `docker kill my-nginx` |
| `docker rm` | Removes a stopped container | `docker rm my-nginx` |
| `docker logs` | Views container logs | `docker logs my-nginx` |
| `docker inspect` | Shows detailed container info | `docker inspect my-nginx` |

---

## � Best Practices  

### ✅ **1. Use `--restart` for Resilient Containers**  
Prevent downtime by automatically restarting failed containers:  
```bash
docker run -d --restart unless-stopped --name my-nginx nginx
```
- `no` (default) → No auto-restart  
- `on-failure` → Restart only on failure  
- `always` → Always restart (even after host reboot)  
- `unless-stopped` → Restart unless manually stopped  

### ✅ **2. Clean Up Unused Containers & Images**  
Avoid disk bloat by removing stopped containers and dangling images:  
```bash
docker container prune   # Remove stopped containers
docker image prune       # Remove unused images
docker system prune      # Clean everything (containers, networks, images)
```

### ✅ **3. Use Read-Only Filesystems for Security**  
Prevent malicious writes by making the container FS read-only:  
```bash
docker run --read-only -d nginx
```
- If the app needs to write, use **volumes**:  
```bash
docker run -v /tmp:/data --read-only -d my-app
```

### ✅ **4. Limit Memory & CPU Usage**  
Prevent a single container from hogging resources:  
```bash
docker run -d --memory="512m" --cpus="1.5" nginx
```

### ✅ **5. Use `.dockerignore` to Optimize Builds**  
Reduce image size by excluding unnecessary files:  
```text
# .dockerignore
node_modules/
.git/
*.log
```

### ✅ **6. Prefer `docker compose` for Multi-Container Apps**  
Instead of running containers manually, define them in `docker-compose.yml`:  
```yaml
version: '3'
services:
  web:
    image: nginx
    ports:
      - "8080:80"
    restart: unless-stopped
  db:
    image: postgres
    environment:
      POSTGRES_PASSWORD: mypassword
```
Then run:  
```bash
docker compose up -d
```

---

## 🔄 Lifecycle Diagram  

```
  [Create] → [Start] → [Running] → [Paused] → [Unpaused] → [Running]
     |           |         |          |            |
     |           |         |          |            |
     v           v         v          v            v
  [Removed] ← [Stopped/Killed] ← [Running] ← [Unpaused]
```

---

## 🚨 Common Pitfalls  

❌ **Running as `root` inside containers** → Use `USER` in Dockerfile  
❌ **Storing data inside containers** → Use **volumes** instead  
❌ **Using `latest` tag in production** → Pin versions (`nginx:1.25`)  
❌ **Exposing unnecessary ports** → Only map required ports (`-p 80:80`)  

---

## 🔍 Debugging Tips  

- **Check logs**: `docker logs -f my-container`  
- **Inspect running processes**: `docker exec -it my-container sh`  
- **View resource usage**: `docker stats`  
- **Check container details**: `docker inspect my-container`  
