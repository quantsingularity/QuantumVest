#!/bin/bash
# QuantumVest Environment Setup Automation Script
# This script automates the environment setup process for QuantumVest
# It handles dependency checking, installation, and environment configuration

# Exit immediately if a command exits with a non-zero status
set -e

# Colors for terminal output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Print banner
echo -e "${BLUE}=================================================${NC}"
echo -e "${GREEN}QuantumVest Environment Setup Automation Script${NC}"
echo -e "${BLUE}=================================================${NC}"

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to check and install system dependencies
check_system_dependencies() {
  echo -e "\n${BLUE}Checking system dependencies...${NC}"

  # List of required system packages
  local required_packages=("curl" "git" "build-essential" "postgresql" "redis-server" "docker" "docker-compose")
  local missing_packages=()

  for package in "${required_packages[@]}"; do
    if ! command_exists "$package"; then
      missing_packages+=("$package")
    fi
  done

  if [ ${#missing_packages[@]} -gt 0 ]; then
    echo -e "${YELLOW}The following packages are missing and will be installed:${NC}"
    for package in "${missing_packages[@]}"; do
      echo "  - $package"
    done

    echo -e "\n${BLUE}Installing missing packages...${NC}"
    sudo apt-get update
    sudo apt-get install -y "${missing_packages[@]}"
  else
    echo -e "${GREEN}All system dependencies are installed.${NC}"
  fi
}

# Function to check and install Python dependencies
setup_python_environment() {
  echo -e "\n${BLUE}Setting up Python environment...${NC}"

  # Check Python version
  if ! command_exists python3; then
    echo -e "${RED}Python 3 is not installed. Installing...${NC}"
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
  fi

  # Create virtual environment if it doesn't exist
  if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating Python virtual environment...${NC}"
    python3 -m venv venv
  fi

  # Activate virtual environment
  echo -e "${BLUE}Activating virtual environment...${NC}"
  source venv/bin/activate

  # Install Python dependencies
  echo -e "${BLUE}Installing Python dependencies...${NC}"
  pip install --upgrade pip

  # Check if requirements.txt exists in backend directory
  if [ -f "code/backend/requirements.txt" ]; then
    pip install -r code/backend/requirements.txt
  else
    echo -e "${YELLOW}Warning: code/backend/requirements.txt not found. Installing common dependencies...${NC}"
    pip install fastapi uvicorn pandas numpy scikit-learn tensorflow pytorch-lightning flask celery redis
  fi

  # Install AI model dependencies
  if [ -f "code/ai_models/requirements.txt" ]; then
    pip install -r code/ai_models/requirements.txt
  fi

  echo -e "${GREEN}Python environment setup complete.${NC}"
}

# Function to set up Node.js environment
setup_node_environment() {
  echo -e "\n${BLUE}Setting up Node.js environment...${NC}"

  # Check if Node.js is installed
  if ! command_exists node; then
    echo -e "${YELLOW}Node.js is not installed. Installing via NVM...${NC}"

    # Install NVM
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.3/install.sh | bash

    # Load NVM
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

    # Install Node.js LTS
    nvm install --lts
    nvm use --lts
  fi

  # Install frontend dependencies
  if [ -d "code/frontend" ]; then
    echo -e "${BLUE}Installing frontend dependencies...${NC}"
    cd code/frontend
    npm install
    cd ../..
  fi

  # Install blockchain dependencies
  if [ -d "code/blockchain" ]; then
    echo -e "${BLUE}Installing blockchain dependencies...${NC}"
    cd code/blockchain
    npm install
    cd ../..
  fi

  # Install mobile frontend dependencies
  if [ -d "mobile-frontend" ]; then
    echo -e "${BLUE}Installing mobile frontend dependencies...${NC}"
    cd mobile-frontend
    npm install
    cd ..
  fi

  echo -e "${GREEN}Node.js environment setup complete.${NC}"
}

# Function to set up environment variables
setup_env_variables() {
  echo -e "\n${BLUE}Setting up environment variables...${NC}"

  # Check if .env file exists
  if [ -f ".env" ]; then
    echo -e "${GREEN}.env file already exists.${NC}"
  else
    echo -e "${YELLOW}.env file not found. Creating from template...${NC}"

    # Create .env file with default values
    cat > .env << EOL
DB_URI="postgresql://user:pass@localhost:5432/investment_platform"
BSC_NODE_URL="wss://bsc-ws-node.nariox.org"
MODEL_DIR="./ai_models"
ALPHA_VANTAGE_KEY="YOUR_API_KEY"
EOL

    echo -e "${GREEN}.env file created. Please update with your actual credentials.${NC}"
  fi

  # Create .env files for frontend and backend if they don't exist
  if [ ! -f "code/frontend/.env" ] && [ -d "code/frontend" ]; then
    echo -e "${YELLOW}Frontend .env file not found. Creating...${NC}"
    cat > code/frontend/.env << EOL
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
REACT_APP_BLOCKCHAIN_ENABLED=false
EOL
    echo -e "${GREEN}Frontend .env file created.${NC}"
  fi

  if [ ! -f "code/backend/.env" ] && [ -d "code/backend" ]; then
    echo -e "${YELLOW}Backend .env file not found. Creating...${NC}"
    cat > code/backend/.env << EOL
DATABASE_URL=postgresql://user:pass@localhost:5432/investment_platform
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=your_jwt_secret_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
ENVIRONMENT=development
EOL
    echo -e "${GREEN}Backend .env file created. Please update with your actual credentials.${NC}"
  fi
}

# Function to set up database
setup_database() {
  echo -e "\n${BLUE}Setting up database...${NC}"

  # Check if PostgreSQL service is running
  if systemctl is-active --quiet postgresql; then
    echo -e "${GREEN}PostgreSQL is running.${NC}"
  else
    echo -e "${YELLOW}PostgreSQL is not running. Starting service...${NC}"
    sudo systemctl start postgresql
  fi

  # Create database and user if they don't exist
  echo -e "${BLUE}Creating database and user if they don't exist...${NC}"

  # Extract database name from DB_URI in .env file
  if [ -f ".env" ]; then
    DB_NAME=$(grep -oP 'DB_URI=.*\/\K[^"]*' .env)

    if [ -n "$DB_NAME" ]; then
      # Check if database exists
      if sudo -u postgres psql -lqt | cut -d \| -f 1 | grep -qw "$DB_NAME"; then
        echo -e "${GREEN}Database $DB_NAME already exists.${NC}"
      else
        echo -e "${YELLOW}Creating database $DB_NAME...${NC}"
        sudo -u postgres createdb "$DB_NAME"
        echo -e "${GREEN}Database $DB_NAME created.${NC}"
      fi
    else
      echo -e "${YELLOW}Could not extract database name from .env file.${NC}"
      echo -e "${YELLOW}Please create the database manually.${NC}"
    fi
  else
    echo -e "${YELLOW}.env file not found. Skipping database creation.${NC}"
  fi
}

# Function to set up Docker containers
setup_docker() {
  echo -e "\n${BLUE}Setting up Docker containers...${NC}"

  # Check if Docker is running
  if systemctl is-active --quiet docker; then
    echo -e "${GREEN}Docker is running.${NC}"
  else
    echo -e "${YELLOW}Docker is not running. Starting service...${NC}"
    sudo systemctl start docker
  fi

  # Check if docker-compose.yml exists
  if [ -f "docker-compose.yml" ]; then
    echo -e "${BLUE}Starting Docker containers...${NC}"
    docker-compose up -d
  elif [ -f "infrastructure/docker-compose.yml" ]; then
    echo -e "${BLUE}Starting Docker containers from infrastructure directory...${NC}"
    cd infrastructure
    docker-compose up -d
    cd ..
  else
    echo -e "${YELLOW}docker-compose.yml not found. Creating a basic one...${NC}"

    # Create a basic docker-compose.yml file
    cat > docker-compose.yml << EOL
version: '3'

services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: investment_platform
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6
    ports:
      - "6379:6379"

volumes:
  postgres_data:
EOL

    echo -e "${GREEN}Basic docker-compose.yml created.${NC}"
    echo -e "${BLUE}Starting Docker containers...${NC}"
    docker-compose up -d
  fi
}

# Main function
main() {
  # Get the project directory
  PROJECT_DIR=$(pwd)

  echo -e "${BLUE}Project directory: $PROJECT_DIR${NC}"

  # Check if we're in the QuantumVest directory
  if [ ! -f "README.md" ] || ! grep -q "QuantumVest" "README.md"; then
    echo -e "${RED}Error: This doesn't appear to be the QuantumVest project directory.${NC}"
    echo -e "${YELLOW}Please run this script from the root of the QuantumVest project.${NC}"
    exit 1
  fi

  # Run the setup functions
  check_system_dependencies
  setup_python_environment
  setup_node_environment
  setup_env_variables
  setup_database
  setup_docker

  echo -e "\n${GREEN}QuantumVest environment setup complete!${NC}"
  echo -e "${BLUE}You can now start the application using:${NC}"
  echo -e "  ./run_quantumvest.sh"
}

# Run the main function
main
