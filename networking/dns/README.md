# Docker DNS: Container Name Resolution

## Example: Web App Connecting to Database

### Step 1: Create a Custom Network
```bash
docker network create myapp-network
```

### Step 2: Start a Database Container
```bash
docker run -d \
  --name database \
  --network myapp-network \
  -e POSTGRES_PASSWORD=secret \
  postgres:13
```

### Step 3: Create a Simple Node.js App
Create `app.js`:
```javascript
const express = require('express');
const { Pool } = require('pg');

const app = express();

// Connect to database using container name!
const pool = new Pool({
  host: 'database',  // ← This is the magic!
  user: 'postgres',
  password: 'secret',
  database: 'postgres'
});

app.get('/', async (req, res) => {
  try {
    const result = await pool.query('SELECT NOW()');
    res.json({ 
      message: 'Connected to database using name "database"!',
      time: result.rows[0].now 
    });
  } catch (err) {
    res.json({ error: err.message });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

### Step 4: Build and Run the App
```bash
# Create Dockerfile
cat > Dockerfile << EOF
FROM node:16-alpine
WORKDIR /app
RUN npm init -y && npm install express pg
COPY app.js .
CMD ["node", "app.js"]
EOF

# Build image
docker build -t myapp .

# Run on same network as database
docker run -d \
  --name webapp \
  --network myapp-network \
  -p 3000:3000 \
  myapp
```

### Step 5: Test the DNS Resolution
```bash
curl http://localhost:3000
```

**Expected output**: JSON with current database time, proving the web app connected to the database using the name `database` instead of an IP address.

### Step 6: See What's Happening
```bash
# Check that containers are on same network
docker network inspect myapp-network

```

## How DNS Works Here

1. **Custom Network**: Docker creates internal DNS for `myapp-network`
2. **Name Resolution**: When webapp code says `host: 'database'`, Docker's DNS resolves it to the database container's IP
3. **Automatic**: No need to find or hardcode IP addresses

## Without DNS (what NOT to do)
```javascript
// BAD: Using IP address
const pool = new Pool({
  host: '172.18.0.2',  // IP could change!
  // ...
});
```

## With DNS (the right way)
```javascript
// GOOD: Using container name
const pool = new Pool({
  host: 'database',  // Always works!
  // ...
});
```

## Key Points

- **Custom Network Required**: Default bridge network doesn't support DNS
- **Container Names = Hostnames**: Use `--name` to set predictable hostnames  
- **No IP Management**: Docker handles everything automatically

## Cleanup
```bash
docker stop webapp database
docker rm webapp database
docker network rm myapp-network
docker rmi myapp
```