#!/bin/bash

# QuantumVest Backend Startup Script

echo "====================================="
echo "QuantumVest Backend Startup"
echo "====================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -q --no-input -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your configuration"
fi

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p ../resources/models
mkdir -p ../resources/data
mkdir -p ../resources/data_cache
mkdir -p ../resources/data/stocks
mkdir -p ../resources/data/crypto

# Initialize database
echo "Initializing database..."
export FLASK_APP=app.py
export FLASK_ENV=development

# Run migrations (if needed)
# flask db init
# flask db migrate
# flask db upgrade

# Start the application
echo "====================================="
echo "Starting QuantumVest Backend..."
echo "Server will be available at: http://localhost:5000"
echo "Health check: http://localhost:5000/api/v1/health"
echo "====================================="

python3 app.py
