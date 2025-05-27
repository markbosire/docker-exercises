
# Docker Container Quickstart Guide

This guide explains how to properly start a Docker container using the `docker run` command, including correct syntax and why order matters.

## Basic `docker run` Command

The correct syntax to start a container is:

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
```

### Example: Running an NGINX Container

```bash
docker run -d --name my-nginx -p 8080:80 nginx
```

## Why Order Matters

1. **Options must come before the image name**  
   Docker interprets everything after the image name as either:
   - A command to run inside the container, or
   - Arguments to that command

2. **Common mistakes**:
   - Putting port mapping (`-p`) after the image name (will fail)
   - Putting environment variables (`-e`) after the image name (will be treated as a command)

## Key Components Explained

| Component       | Placement          | Example             | Purpose |
|-----------------|--------------------|---------------------|---------|
| Options         | Before image name  | `-d`, `-p`, `--name`| Configure container behavior |
| Image name      | After options      | `nginx`             | Specifies which image to use |
| Command         | After image name   | `bash`              | Overrides default CMD in image |
| Arguments       | After command      | `-c "echo hello"`   | Passed to the command |

## Common Examples

### 1. Basic container with port mapping
```bash
docker run -d -p 8080:80 --name webserver nginx
```
- `-d`: Run in detached mode
- `-p 8080:80`: Map host port 8080 to container port 80
- `--name webserver`: Give the container a name
- `nginx`: The image to use

### 2. Container with environment variables
```bash
docker run -e "ENV_VAR=value" -p 3000:3000 node
```

### 3. Overriding the default command
```bash
docker run ubuntu sleep 30
```
- Runs `sleep 30` instead of Ubuntu's default command

## Troubleshooting

If your container isn't starting:
1. Check if options are before the image name
2. Verify correct port mapping (host:container)
3. Check logs: `docker logs [CONTAINER_NAME]`
4. List all containers (including stopped ones): `docker ps -a`

