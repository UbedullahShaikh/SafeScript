#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Helper function for logging
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Trap errors
trap 'error "An error occurred on line $LINENO. Exiting..."; exit 1' ERR

log "Starting setup process..."

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    error "Python 3 is not installed. Please install it and try again."
    exit 1
fi

# Create virtual environment
log "Creating virtual environment..."
if [ -d "venv" ]; then
    log "Virtual environment 'venv' already exists. Skipping creation."
else
    python3 -m venv venv
    log "Virtual environment created."
fi

# Install dependencies
log "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    ./venv/bin/pip install -r requirements.txt
    log "Dependencies installed successfully."
else
    error "requirements.txt not found!"
    exit 1
fi

log "Setup complete!"
echo -e "${GREEN}To activate the virtual environment, run:${NC} source venv/bin/activate"
