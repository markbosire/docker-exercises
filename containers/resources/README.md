# Docker Resource Management Guide  
**How to Control CPU, Memory, and I/O Usage for Containers**  

This guide covers best practices for managing container resources, including setting limits for CPU, memory, and disk I/O to prevent single containers from hogging system resources.  

---

## 🧠 **Memory Management**  

### **1. Set Hard Memory Limit**  
Prevent a container from using more than a specified amount of RAM:  
```bash
docker run -d --memory="1g" --name my-container nginx
```  
- `1g` = 1 GB (also supports `m` for MB, e.g., `512m`)  
- The container is **killed** if it exceeds this limit.  

### **2. Set Memory + Swap Limit**  
Control both RAM and swap usage:  
```bash
docker run -d --memory="1g" --memory-swap="2g" my-container
```  
*(Swap = RAM + Disk Swap Space)*  

### **3. Soft Memory Limit (OOM Priority)**  
Set a soft limit that triggers warnings but doesn’t kill the container:  
```bash
docker run -d --memory-reservation="750m" --memory="1g" nginx
```  

---

## ⚡ **CPU Management**  

### **1. Limit CPU Cores**  
Restrict a container to use only **1 CPU core**:  
```bash
docker run -d --cpus="1.5" --name my-container nginx
```  
- `1.5` = 1.5 CPU cores (fractional values allowed)  

### **2. Pin to Specific CPU Cores**  
Assign containers to specific CPUs (useful for NUMA systems):  
```bash
docker run -d --cpuset-cpus="0,2" nginx
```  
*(Uses only CPU cores 0 and 2)*  

### **3. CPU Priority (Weight)**  
Adjust CPU shares (relative priority):  
```bash
docker run -d --cpu-shares="512" nginx
```  
- Default = `1024`  
- A container with `512` gets **half** the CPU time of the default.  

---

## 📊 **Disk & I/O Limits**  

### **1. Limit Disk Read/Write Speed**  
Prevent a container from saturating disk I/O:  
```bash
docker run -d \
  --device-read-bps="/dev/sda:1mb" \
  --device-write-bps="/dev/sda:1mb" \
  --name my-container nginx
```  
- Limits disk I/O to **1 MB/s**  

### **2. Restrict IOPS (Input/Output Operations Per Second)**  
```bash
docker run -d \
  --device-read-iops="/dev/sda:100" \
  --device-write-iops="/dev/sda:100" \
  nginx
```  
- Max **100 read/write operations per second**  

---

## 🛠️ **Monitoring Resource Usage**  

### **1. Live Stats Dashboard**  
```bash
docker stats
```  
**Output:**  
```
CONTAINER ID   NAME       CPU %     MEM USAGE / LIMIT     MEM %     NET I/O       BLOCK I/O     PIDS
a1b2c3d4e5f6   my-nginx   0.15%     250MiB / 1GiB        25%       1.5kB / 0B    0B / 0B       3
```  

### **2. Check Specific Container Limits**  
```bash
docker inspect -f "{{ .HostConfig.Memory }}" my-container
```  

---

## 🚨 **Troubleshooting Resource Issues**  

| Symptom | Possible Cause | Fix |
|---------|---------------|-----|
| **Container killed** | OOM (Out of Memory) | Increase `--memory` or optimize app |
| **High CPU usage** | No CPU limit set | Use `--cpus="1.0"` |
| **Slow disk I/O** | Other containers hogging disk | Set `--device-read-bps` limits |
| **Processes frozen** | Memory swap exhaustion | Increase `--memory-swap` |

---

## ✅ **Best Practices**  

1. **Always set memory limits** → Prevents system crashes.  
2. **Use `--restart=unless-stopped`** → Auto-recover if killed by OOM.  
3. **Monitor with `docker stats`** → Detect leaks early.  
4. **Avoid unlimited CPU** → Prevents noisy neighbors.  

---

## 🎯 **Example: Running a Resource-Constrained Web Server**  
```bash
docker run -d \
  --name my-nginx \
  --memory="512m" \
  --memory-swap="1g" \
  --cpus="1.0" \
  --cpu-shares="512" \
  -p 80:80 \
  nginx
```

