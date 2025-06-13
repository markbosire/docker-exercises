# Docker Environment Variables & .env Files Tutorial

## Purpose
Environment variables in Docker Compose allow you to configure applications without hardcoding values, making your containers portable across different environments (development, staging, production).

## Step-by-Step Implementation

### Step 1: Create a .env file
Create `.env` in your project root:
```env
# Database configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=myapp
DB_USER=admin
DB_PASSWORD=secret123

# Application settings
APP_ENV=development
APP_PORT=3000
```

### Step 2: Reference variables in docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    image: nginx
    ports:
      - "${APP_PORT}:80"
    environment:
      - ENV=${APP_ENV}
    
  database:
    image: postgres:13
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    ports:
      - "${DB_PORT}:5432"
```

### Step 3: Override with system environment variables
```bash
# Override specific values
DB_PASSWORD=production_secret docker-compose up

# Or export first
export DB_PASSWORD=production_secret
docker-compose up
```

### Step 4: Use env_file for external files
```yaml
services:
  web:
    image: myapp
    env_file:
      - .env.local
      - .env.shared
```

## Best Practices

1. **Never commit sensitive .env files** - Add to `.gitignore`
2. **Use .env.example** for documenting required variables
3. **System variables override .env values**
4. **Use quotes for values with spaces**: `MESSAGE="Hello World"`
5. **No spaces around =**: `KEY=value` not `KEY = value`

## Example Project Structure
```
project/
├── docker-compose.yml
├── .env
├── .env.example
├── .env.production
└── .gitignore
```

## Quick Commands
```bash
# Start with specific env file
docker-compose --env-file .env.production up

# Check resolved values
docker-compose config

# Override single variable
API_KEY=xyz123 docker-compose up
```

## When to Use Each Method

### Use `.env` files when:
- Setting default values for multiple services
- Sharing common configuration across environments
- Keeping sensitive data out of docker-compose.yml

### Use inline environment variables when:
- Service-specific configuration
- Overriding .env values
- Simple, non-sensitive values