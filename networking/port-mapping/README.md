# Docker Port Mapping 


Create `app.py`:
```python
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler

class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, service_name, port, *args, **kwargs):
        self.service_name = service_name
        self.port = port
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = f'''
        <h1>{self.service_name}</h1>
        <p>Running on container port {self.port}</p>
        <p>Service: {self.service_name}</p>
        <hr>
        <p>Try the other services:</p>
        <ul>
            <li><a href="http://localhost:3000">Web App (port 3000)</a></li>
            <li><a href="http://localhost:4000">API (port 4000)</a></li>
            <li><a href="http://localhost:5000">Admin (port 5000)</a></li>
        </ul>
        '''
        self.wfile.write(html.encode())

def run_server(service_name, port):
    handler = lambda *args, **kwargs: MyHandler(service_name, port, *args, **kwargs)
    with HTTPServer(("", port), handler) as httpd:
        print(f"{service_name} running on port {port}")
        httpd.serve_forever()

# Start three services on different ports
services = [
    ("Web App", 8000),
    ("API Service", 8001), 
    ("Admin Panel", 8002)
]

# Run first two services in background threads
for service_name, port in services[:-1]:
    thread = threading.Thread(target=run_server, args=(service_name, port), daemon=True)
    thread.start()

# Run the last service in main thread
run_server(services[-1][0], services[-1][1])
```

## Step 2: Create Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY app.py .
EXPOSE 8000 8001 8002
CMD ["python", "app.py"]
```

**Key Points**: 
- `EXPOSE` documents which ports the container uses, but doesn't publish them
- Multiple ports can be exposed
- This is just documentation - actual mapping happens with `-p` flag

## Step 3: Build the Image

```bash
docker build -t my-web-app .
```

## Step 4: Understanding Multiple Port Mapping

### The Problem: Run Without Port Mapping
```bash
docker run my-web-app
```
- Container runs with 3 services but you can't access any of them
- All services are isolated inside the container

### The Solution: Map Multiple Ports
```bash
docker run -p 3000:8000 -p 4000:8001 -p 5000:8002 my-web-app
```

**Port Mapping Breakdown**:
- `-p 3000:8000` → Web App: host port 3000 → container port 8000
- `-p 4000:8001` → API Service: host port 4000 → container port 8001  
- `-p 5000:8002` → Admin Panel: host port 5000 → container port 8002

## Step 5: Test All Services

Open your browser and test all three services:

1. **Web App**: `http://localhost:3000`
2. **API Service**: `http://localhost:4000` 
3. **Admin Panel**: `http://localhost:5000`

Each page will show which service you're accessing and provide links to the others.

## Step 6: Experiment with Different Mappings

Stop the container (Ctrl+C) and try different host port mappings:

```bash
# Map to different host ports
docker run -p 8080:8000 -p 8081:8001 -p 8082:8002 my-web-app
```

Now access:
- `http://localhost:8080` (Web App)
- `http://localhost:8081` (API Service)
- `http://localhost:8082` (Admin Panel)

```bash
# Map some services to same port numbers
docker run -p 8000:8000 -p 9000:8001 -p 9001:8002 my-web-app
```

## Step 7: Understanding What Happens

When you run the container with multiple port mappings:

```bash
docker run -p 3000:8000 -p 4000:8001 -p 5000:8002 my-web-app
```

**Inside the container**: 3 services run on ports 8000, 8001, 8002
**On your host**: Docker forwards traffic from ports 3000, 4000, 5000 to the container

```
Your Browser → localhost:3000 → Docker → Container:8000 → Web App
Your Browser → localhost:4000 → Docker → Container:8001 → API Service  
Your Browser → localhost:5000 → Docker → Container:8002 → Admin Panel
```

## Key Concepts Summary

1. **EXPOSE** in Dockerfile = documentation only (tells others which ports the app uses)
2. **-p HOST:CONTAINER** = actual port mapping (makes ports accessible)
3. **Multiple mappings** = use multiple -p flags
4. **Port conflicts** = can't map different containers to same host port
5. **One-to-one mapping** = each host port maps to exactly one container port

## Common Commands

```bash
# See running containers and their port mappings
docker ps

# Run in background (detached)
docker run -d -p 3000:8000 -p 4000:8001 -p 5000:8002 my-web-app

# Stop container
docker stop <container_id>

# Map all exposed ports to random available host ports
docker run -P my-web-app

# Check which ports Docker assigned
docker port <container_id>
```

## Quick Exercise

1. Run the container with `-P` flag instead of explicit `-p` mappings:
   ```bash
   docker run -P my-web-app
   ```

2. Use `docker ps` to see which random ports Docker assigned

3. Access the services using those random ports!