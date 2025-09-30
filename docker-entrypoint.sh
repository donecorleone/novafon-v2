#!/bin/bash

# Start backend in background
echo "Starting FastAPI backend..."
python main.py &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend to start..."
sleep 5

# Check if backend is running
if ! curl -f http://localhost:8000/products > /dev/null 2>&1; then
    echo "Backend failed to start"
    exit 1
fi

echo "Backend started successfully"

# Start frontend (if needed for development)
# For production, you might want to serve static files with nginx instead
echo "Application is ready!"
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:4321"

# Keep container running
wait $BACKEND_PID
