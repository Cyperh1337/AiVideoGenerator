#!/bin/bash

echo "========================================"
echo "  ComfyUI Video Generator - Starting..."
echo "========================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Backend Server...${NC}"
cd "$(dirname "$0")/backend"

# Check if virtual environment exists
if [ -d "../venv" ]; then
    echo -e "${GREEN}Using virtual environment...${NC}"
    source ../venv/bin/activate
fi

# Start backend in background
python server.py &
BACKEND_PID=$!

echo -e "${BLUE}Waiting for backend to start...${NC}"
sleep 5

echo -e "${BLUE}Starting Frontend...${NC}"
cd ../frontend
npm start &
FRONTEND_PID=$!

echo ""
echo "========================================"
echo "  ComfyUI Video Generator Started!"
echo "========================================"
echo ""
echo -e "${GREEN}Backend API: http://localhost:8001${NC}"
echo -e "${GREEN}Frontend:    http://localhost:3000${NC}"
echo ""
echo -e "${YELLOW}IMPORTANTE: Assicurati che ComfyUI sia in esecuzione su:${NC}"
echo -e "${YELLOW}http://127.0.0.1:8188${NC}"
echo ""
echo -e "${BLUE}Premi Ctrl+C per fermare tutto...${NC}"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}Stopping ComfyUI Video Generator...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo -e "${GREEN}Stopped.${NC}"
    exit 0
}

# Trap Ctrl+C
trap cleanup INT

# Wait for processes
wait