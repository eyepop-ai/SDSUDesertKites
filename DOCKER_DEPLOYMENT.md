# Docker Deployment Guide

## Overview
This guide explains how to run the Desert Kite Detection Streamlit app using Docker.

---

## Prerequisites

- Docker installed on your system ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (usually included with Docker Desktop)
- Your API keys ready:
  - Google Maps API Key (optional, hardcoded fallback exists)
  - EyePop API Key (entered via the app's authentication screen)

---

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. **Set up environment variables** (optional):
   ```bash
   # Create a .env file
   echo "GOOGLE_MAPS_API_KEY=your_google_maps_key_here" > .env
   ```

2. **Build and run**:
   ```bash
   docker-compose up -d
   ```

3. **Access the app**:
   Open your browser and go to: `http://localhost:8501`

4. **Stop the app**:
   ```bash
   docker-compose down
   ```

---

### Option 2: Using Docker CLI

1. **Build the image**:
   ```bash
   docker build -t desert-kite-detection .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name desert-kite-detection \
     -p 8501:8501 \
     -v $(pwd)/temp_streamlit:/app/temp_streamlit \
     -v $(pwd)/results:/app/results \
     -e GOOGLE_MAPS_API_KEY=your_key_here \
     desert-kite-detection
   ```

3. **Access the app**:
   Open your browser and go to: `http://localhost:8501`

4. **Stop the container**:
   ```bash
   docker stop desert-kite-detection
   docker rm desert-kite-detection
   ```

---

## Docker Commands Reference

### Building

```bash
# Build the image
docker build -t desert-kite-detection .

# Build with no cache (fresh build)
docker build --no-cache -t desert-kite-detection .
```

### Running

```bash
# Run in foreground (see logs)
docker run -p 8501:8501 desert-kite-detection

# Run in background (detached)
docker run -d -p 8501:8501 --name kite-app desert-kite-detection

# Run with environment variables
docker run -d -p 8501:8501 \
  -e GOOGLE_MAPS_API_KEY=your_key \
  --name kite-app \
  desert-kite-detection

# Run with volume mounts (for persistent data)
docker run -d -p 8501:8501 \
  -v $(pwd)/temp_streamlit:/app/temp_streamlit \
  -v $(pwd)/results:/app/results \
  --name kite-app \
  desert-kite-detection
```

### Managing Containers

```bash
# View running containers
docker ps

# View all containers (including stopped)
docker ps -a

# View logs
docker logs kite-app

# Follow logs in real-time
docker logs -f kite-app

# Stop container
docker stop kite-app

# Start stopped container
docker start kite-app

# Restart container
docker restart kite-app

# Remove container
docker rm kite-app

# Remove container (force)
docker rm -f kite-app
```

### Managing Images

```bash
# List images
docker images

# Remove image
docker rmi desert-kite-detection

# Remove unused images
docker image prune

# Remove all unused images
docker image prune -a
```

---

## Docker Compose Commands

```bash
# Build and start services
docker-compose up

# Build and start in background
docker-compose up -d

# Build without cache
docker-compose build --no-cache

# View logs
docker-compose logs

# Follow logs
docker-compose logs -f

# Stop services
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop, remove containers, and remove volumes
docker-compose down -v

# Restart services
docker-compose restart
```

---

## Configuration

### Environment Variables

The app supports the following environment variables:

- `GOOGLE_MAPS_API_KEY`: Your Google Maps API key (optional, has fallback)
- `PORT`: The port to run the app on (default: 8501)

**Setting environment variables:**

1. **Using .env file** (recommended for docker-compose):
   ```bash
   # .env
   GOOGLE_MAPS_API_KEY=your_key_here
   ```

2. **Using -e flag** (for docker run):
   ```bash
   docker run -e GOOGLE_MAPS_API_KEY=your_key ...
   ```

3. **Using environment section in docker-compose.yml**:
   ```yaml
   environment:
     - GOOGLE_MAPS_API_KEY=your_key_here
   ```

### Volumes

The container creates two directories for data:
- `/app/temp_streamlit`: Temporary satellite images
- `/app/results`: Detection results

**To persist data**, mount these as volumes:
```bash
-v $(pwd)/temp_streamlit:/app/temp_streamlit
-v $(pwd)/results:/app/results
```

---

## Port Configuration

The app runs on port **8501** by default.

**To use a different port:**

1. **Docker CLI**:
   ```bash
   docker run -p 3000:8501 desert-kite-detection
   ```
   Access at: `http://localhost:3000`

2. **Docker Compose**:
   ```yaml
   ports:
     - "3000:8501"
   ```

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker logs desert-kite-detection

# Check if port is in use
lsof -i :8501  # macOS/Linux
netstat -ano | findstr :8501  # Windows
```

### Can't access the app

1. Check if container is running:
   ```bash
   docker ps
   ```

2. Check if port is correctly mapped:
   ```bash
   docker port desert-kite-detection
   ```

3. Try accessing via container IP:
   ```bash
   docker inspect desert-kite-detection | grep IPAddress
   ```

### Image build fails

```bash
# Clean build with no cache
docker build --no-cache -t desert-kite-detection .

# Check Docker disk space
docker system df

# Clean up unused resources
docker system prune
```

### Permission issues with volumes

```bash
# On Linux, you may need to set permissions
chmod -R 777 temp_streamlit results
```

---

## Production Deployment

### Optimization

1. **Use multi-stage builds** (already optimized in Dockerfile)
2. **Minimize image size** (using slim Python image)
3. **Use .dockerignore** (already configured)

### Security

1. **Don't commit .env files**:
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use secrets management** for production:
   - Docker secrets
   - Kubernetes secrets
   - Cloud provider secret managers

3. **Run as non-root user** (optional enhancement):
   ```dockerfile
   RUN useradd -m -u 1000 appuser
   USER appuser
   ```

### Health Checks

The Dockerfile includes a health check:
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' desert-kite-detection
```

---

## Cloud Deployment

### Google Cloud Run

```bash
# Build and push to Google Container Registry
docker build -t gcr.io/YOUR_PROJECT_ID/desert-kite-detection .
docker push gcr.io/YOUR_PROJECT_ID/desert-kite-detection

# Deploy to Cloud Run
gcloud run deploy desert-kite-detection \
  --image gcr.io/YOUR_PROJECT_ID/desert-kite-detection \
  --platform managed \
  --port 8501 \
  --set-env-vars GOOGLE_MAPS_API_KEY=your_key
```

### AWS ECS / Fargate

```bash
# Build and push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
docker build -t desert-kite-detection .
docker tag desert-kite-detection:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/desert-kite-detection:latest
docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/desert-kite-detection:latest
```

### Azure Container Instances

```bash
# Push to Azure Container Registry
az acr login --name yourregistry
docker build -t yourregistry.azurecr.io/desert-kite-detection .
docker push yourregistry.azurecr.io/desert-kite-detection
```

### Heroku

```bash
# Login to Heroku container registry
heroku container:login

# Build and push
heroku container:push web -a your-app-name

# Release
heroku container:release web -a your-app-name
```

---

## Development

### Live Reload (for development)

```bash
# Mount app.py for live editing
docker run -d -p 8501:8501 \
  -v $(pwd)/app.py:/app/app.py \
  --name kite-dev \
  desert-kite-detection
```

### Interactive Shell

```bash
# Access container shell
docker exec -it desert-kite-detection /bin/bash

# Run Python interactively
docker exec -it desert-kite-detection python
```

---

## Cleanup

### Remove everything

```bash
# Stop and remove containers
docker-compose down

# Remove images
docker rmi desert-kite-detection

# Remove volumes
docker volume prune

# Remove everything (nuclear option)
docker system prune -a --volumes
```

---

## Image Size

The Docker image is optimized for size:
- Using `python:3.11-slim` base image
- Multi-stage build (if needed)
- `.dockerignore` to exclude unnecessary files
- No cache for pip installs

**Expected image size:** ~500MB - 800MB

---

## Support

For issues with:
- **Docker**: Check [Docker documentation](https://docs.docker.com)
- **Streamlit**: Check [Streamlit documentation](https://docs.streamlit.io)
- **App-specific**: Check the main README.md

---

## Summary

**Quick commands for daily use:**

```bash
# Start the app
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the app
docker-compose down

# Access the app
open http://localhost:8501
```

That's it! Your Desert Kite Detection app is now running in Docker. 🐳🪁

