# Docker Interactive Mode Troubleshooting Guide  

This guide explains how to use **interactive mode** to troubleshoot running containers by accessing shells, running commands, and debugging live issues.  

---

## 🖥️ **Accessing an Interactive Shell**  

### **1. Start a New Container in Interactive Mode**  
Run a container with an interactive terminal (`-it` flag):  
```bash
docker run -it --name my-container ubuntu /bin/bash
```  
- `-i` → Keeps STDIN open (interactive)  
- `-t` → Allocates a pseudo-TTY (terminal)  
- `/bin/bash` → Default shell (can use `/bin/sh` for Alpine)  

### **2. Attach to a Running Container**  
Get a shell inside an already-running container:  
```bash
docker exec -it <container_name_or_id> /bin/bash
```  
Example:  
```bash
docker exec -it my-nginx /bin/sh
```  
*(Use `/bin/sh` for Alpine-based images like NGINX)*  

---

## 🔍 **Common Troubleshooting Commands**  

Once inside the container, use these Linux commands:  

| Command | Purpose | Example |
|---------|---------|---------|
| `ls` | List files | `ls -la /etc/nginx` |
| `cat` | View file contents | `cat /var/log/nginx/error.log` |
| `ps` | Check running processes | `ps aux` |
| `netstat` | List open ports | `netstat -tuln` |
| `curl` | Test HTTP endpoints | `curl http://localhost:80` |
| `ping` | Check network connectivity | `ping google.com` |
| `env` | View environment variables | `env` |
| `df -h` | Check disk space | `df -h` |
| `top` / `htop` | Monitor live processes | `top` |

---

## 🛠️ **Debugging Workflow**  

### **1. Inspect Service Logs**  
Check application-specific logs:  
```bash
cat /var/log/<service>.log
```  
Example for NGINX:  
```bash
cat /var/log/nginx/error.log
```

### **2. Verify Config Files**  
Check if configurations are correct:  
```bash
cat /etc/<service>/config.conf
```  
Example for NGINX:  
```bash
cat /etc/nginx/nginx.conf
```

### **3. Test Network Connectivity**  
Check if the container can reach external services:  
```bash
ping google.com
curl -I http://localhost:80
```

### **4. Check Running Processes**  
See what’s actively running:  
```bash
ps aux | grep nginx
```

### **5. Validate Environment Variables**  
Ensure required variables are set:  
```bash
env | grep DB_
```

---

## 🚨 **Common Issues & Fixes**  

### **❌ "No such file or directory"**  
- **Cause**: Missing executable or wrong path  
- **Fix**: Verify with `ls` and check Dockerfile `CMD`  

### **❌ "Permission Denied"**  
- **Cause**: Running as non-root without permissions  
- **Fix**: Use `chmod` or run as root (`docker exec -u root -it ...`)  

### **❌ "Connection Refused"**  
- **Cause**: Service not running or wrong port  
- **Fix**: Check `netstat -tuln` and restart the service  

### **❌ "Executable not found in $PATH"**  
- **Cause**: Missing package in the container  
- **Fix**: Install it (`apt-get install curl -y`)  

---

## 📌 **Best Practices**  

✅ **Use `--rm` for temporary debugging containers** → Auto-delete on exit:  
```bash
docker run -it --rm ubuntu /bin/bash
```  

✅ **Prefer `exec` over `attach`** → `exec` creates a new session, while `attach` connects to the existing one (can lock the terminal).  

✅ **Keep containers minimal** → Install only debugging tools you need (`curl`, `ping`, `vim`).  

✅ **Use `docker cp` to transfer files** → Copy logs/configs out for analysis:  
```bash
docker cp my-container:/var/log/nginx/error.log ./debug.log
```  

---

## 🎯 **Example Workflow**  

1. **Start a failing container**:  
   ```bash
   docker run -d --name my-app my-broken-app
   ```  

2. **Attach to debug**:  
   ```bash
   docker exec -it my-app /bin/sh
   ```  

3. **Check logs**:  
   ```bash
   cat /app/logs/error.log
   ```  

4. **Test fixes**:  
   ```bash
   echo "DEBUG=true" >> /app/.env
   ```  

5. **Restart the service**:  
   ```bash
   kill -HUP 1  # Reload main process (PID 1)
   ```  

6. **Exit & clean up**:  
   ```bash
   exit
   docker rm -f my-app
   ```  

---

## 🔥 **Pro Tips**  

- **For Alpine-based images**: Use `/bin/sh` (no Bash).  
- **For Windows containers**: Use `docker exec -it cmd` or `powershell`.  
- **No shell?** → Debug with `docker logs` or override `ENTRYPOINT`:  
  ```bash
  docker run -it --entrypoint /bin/sh my-image
  ```  


