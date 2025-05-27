# Docker Logs & Real-Time Monitoring  

This guide covers how to **view logs** and **monitor container stats** in real-time for effective debugging and performance analysis.  

---

## 📜 Viewing Container Logs  

### **1. Basic Logs**  
View the logs of a container:  
```bash
docker logs <container_name_or_id>
```  
Example:  
```bash
docker logs my-nginx
```

### **2. Follow Logs in Real-Time**  
Stream logs continuously (similar to `tail -f`):  
```bash
docker logs -f <container_name_or_id>
```  
Example:  
```bash
docker logs -f my-nginx
```

### **3. Show Recent Logs & Tail**  
Display the last **N** lines and follow:  
```bash
docker logs --tail 50 -f <container_name_or_id>
```  
Example:  
```bash
docker logs --tail 100 -f my-app
```

### **4. Timestamps in Logs**  
Include timestamps for better debugging:  
```bash
docker logs -t <container_name_or_id>
```  
Example:  
```bash
docker logs -tf my-nginx
```

### **5. Filter Logs by Time**  
Show logs since a specific time:  
```bash
docker logs --since 2024-05-01T00:00:00 <container_name_or_id>
```  
Example:  
```bash
docker logs --since 1h -f my-app  # Last 1 hour
```

---

## 📊 Monitoring Container Stats in Real-Time  

### **1. Live Resource Usage (CPU, Memory, Network, Disk)**  
View real-time stats for all running containers:  
```bash
docker stats
```  
Example output:  
```
CONTAINER ID   NAME       CPU %     MEM USAGE / LIMIT     MEM %     NET I/O       BLOCK I/O   PIDS
a1b2c3d4e5f6   my-nginx   0.05%     25MiB / 1GiB         2.50%     1.2kB / 0B    0B / 0B     3
```

### **2. Monitor Specific Containers**  
Track stats for selected containers:  
```bash
docker stats <container1> <container2>
```  
Example:  
```bash
docker stats my-nginx my-postgres
```

### **3. No-Stream (Single Snapshot)**  
Get a one-time stats snapshot instead of a live stream:  
```bash
docker stats --no-stream
```

### **4. Format Stats Output**  
Customize stats display (e.g., only CPU and memory):  
```bash
docker stats --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"
```  
Example with custom columns:  
```bash
docker stats --format "table {{.ID}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemPerc}}"
```

---

## 🛠️ Advanced Debugging  

### **1. View Processes Inside a Container**  
Check running processes:  
```bash
docker top <container_name_or_id>
```  
Example:  
```bash
docker top my-nginx
```

### **2. Interactive Shell for Troubleshooting**  
Access a shell inside the container:  
```bash
docker exec -it <container_name_or_id> sh  # (or bash)
```  
Example:  
```bash
docker exec -it my-nginx sh
```

### **3. Inspect Container Details**  
Get full container metadata (IP, mounts, configs, etc.):  
```bash
docker inspect <container_name_or_id>
```  
Example (filter for specific info):  
```bash
docker inspect -f '{{ .NetworkSettings.IPAddress }}' my-nginx
```

---

## 🔥 Pro Tips  

✅ **Combine `logs` + `stats` for debugging** → Run in separate terminals  
✅ **Use `grep` to filter logs** → `docker logs my-app | grep "ERROR"`  
✅ **Log drivers** → Configure Docker to send logs to `json-file`, `syslog`, or `fluentd`  
✅ **For production** → Use tools like **Prometheus + Grafana** or **ELK Stack** for advanced monitoring  

---

## 📝 Example Workflow  

1. **Start a container**  
   ```bash
   docker run -d --name my-web -p 8080:80 nginx
   ```

2. **Check live logs**  
   ```bash
   docker logs -f my-web
   ```

3. **Monitor performance**  
   ```bash
   docker stats my-web
   ```

4. **Debug issues**  
   ```bash
   docker exec -it my-web sh
   ```


