#!/bin/bash

echo "========================================"
echo "  ComfyUI Video Generator - Installer"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python3 non trovato. Installazione in corso...${NC}"
    
    # Detect OS and install Python
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        # Linux
        if command -v apt &> /dev/null; then
            sudo apt update
            sudo apt install -y python3 python3-pip python3-venv
        elif command -v yum &> /dev/null; then
            sudo yum install -y python3 python3-pip
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3 python3-pip
        else
            echo -e "${RED}Package manager non supportato. Installa Python3 manualmente.${NC}"
            exit 1
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install python3
        else
            echo -e "${RED}Homebrew non trovato. Installa Python3 manualmente da python.org${NC}"
            exit 1
        fi
    else
        echo -e "${RED}OS non supportato${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}Python3 installato!${NC}"
fi

# Make script executable
chmod +x setup.py

# Run Python installer
echo -e "${BLUE}Avvio installazione automatica...${NC}"
python3 setup.py

echo ""
echo -e "${GREEN}Installazione completata!${NC}"
echo ""
echo -e "${YELLOW}Per avviare l'app, esegui: ./start.sh${NC}"
echo ""