#!/bin/bash
# Quick start script for Docker deployment

echo "🐳 Starting Desert Kite Detection App with Docker..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    echo "✓ Using Docker Compose..."
    docker-compose up -d
    
    echo ""
    echo "✅ App is starting..."
    echo "📱 Access the app at: http://localhost:8501"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
else
    echo "✓ Using Docker CLI..."
    
    # Build if image doesn't exist
    if [[ "$(docker images -q desert-kite-detection 2> /dev/null)" == "" ]]; then
        echo "Building Docker image..."
        docker build -t desert-kite-detection .
    fi
    
    # Stop and remove existing container if running
    docker stop desert-kite-detection 2>/dev/null
    docker rm desert-kite-detection 2>/dev/null
    
    # Run the container
    docker run -d \
        --name desert-kite-detection \
        -p 8501:8501 \
        -v "$(pwd)/temp_streamlit:/app/temp_streamlit" \
        -v "$(pwd)/results:/app/results" \
        desert-kite-detection
    
    echo ""
    echo "✅ App is starting..."
    echo "📱 Access the app at: http://localhost:8501"
    echo ""
    echo "To view logs: docker logs -f desert-kite-detection"
    echo "To stop: docker stop desert-kite-detection"
fi

echo ""
echo "🪁 Desert Kite Detection is ready!"

