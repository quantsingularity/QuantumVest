#!/bin/bash
# QuantumVest Deployment Automation Script
# This script automates the deployment process for QuantumVest
# It handles Docker container management, database initialization, and service orchestration

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
echo -e "${GREEN}QuantumVest Deployment Automation Script${NC}"
echo -e "${BLUE}=================================================${NC}"

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to deploy Docker containers
deploy_docker() {
  echo -e "\n${BLUE}Deploying Docker containers...${NC}"
  
  # Check if Docker is installed
  if ! command_exists docker; then
    echo -e "${RED}Error: Docker is not installed.${NC}"
    echo -e "${YELLOW}Please install Docker before proceeding.${NC}"
    exit 1
  fi
  
  # Check if Docker is running
  if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker daemon is not running.${NC}"
    echo -e "${YELLOW}Please start Docker before proceeding.${NC}"
    exit 1
  fi
  
  # Check if docker-compose is installed
  if ! command_exists docker-compose; then
    echo -e "${RED}Error: docker-compose is not installed.${NC}"
    echo -e "${YELLOW}Please install docker-compose before proceeding.${NC}"
    exit 1
  fi
  
  # Check if docker-compose.yml exists
  if [ -f "docker-compose.yml" ]; then
    echo -e "${BLUE}Using docker-compose.yml in the current directory...${NC}"
    docker-compose down
    docker-compose build
    docker-compose up -d
  elif [ -f "infrastructure/docker-compose.yml" ]; then
    echo -e "${BLUE}Using docker-compose.yml in the infrastructure directory...${NC}"
    cd infrastructure
    docker-compose down
    docker-compose build
    docker-compose up -d
    cd ..
  else
    echo -e "${RED}Error: docker-compose.yml not found.${NC}"
    echo -e "${YELLOW}Please create a docker-compose.yml file before proceeding.${NC}"
    exit 1
  fi
  
  echo -e "${GREEN}Docker containers deployed successfully.${NC}"
}

# Function to initialize database
initialize_database() {
  echo -e "\n${BLUE}Initializing database...${NC}"
  
  # Check if backend directory exists
  if [ ! -d "code/backend" ]; then
    echo -e "${RED}Error: Backend directory not found.${NC}"
    echo -e "${YELLOW}Please ensure the backend directory exists before proceeding.${NC}"
    exit 1
  fi
  
  # Check if database migration scripts exist
  if [ -f "code/backend/migrations/run_migrations.py" ]; then
    echo -e "${BLUE}Running database migrations...${NC}"
    cd code/backend
    python migrations/run_migrations.py
    cd ../..
  elif [ -f "code/backend/alembic.ini" ]; then
    echo -e "${BLUE}Running Alembic migrations...${NC}"
    cd code/backend
    
    # Check if alembic is installed
    if ! command_exists alembic; then
      echo -e "${YELLOW}Alembic not found. Installing...${NC}"
      pip install alembic
    fi
    
    alembic upgrade head
    cd ../..
  else
    echo -e "${YELLOW}No migration scripts found. Skipping database initialization.${NC}"
    echo -e "${YELLOW}Please initialize the database manually if needed.${NC}"
  fi
  
  echo -e "${GREEN}Database initialization completed.${NC}"
}

# Function to deploy backend services
deploy_backend() {
  echo -e "\n${BLUE}Deploying backend services...${NC}"
  
  # Check if backend directory exists
  if [ ! -d "code/backend" ]; then
    echo -e "${RED}Error: Backend directory not found.${NC}"
    echo -e "${YELLOW}Please ensure the backend directory exists before proceeding.${NC}"
    exit 1
  fi
  
  # Check if we're deploying in Docker or directly
  if [ "$DEPLOY_MODE" = "docker" ]; then
    echo -e "${BLUE}Backend services are deployed via Docker.${NC}"
    echo -e "${BLUE}No additional action needed.${NC}"
  else
    echo -e "${BLUE}Deploying backend services directly...${NC}"
    
    # Check if Python virtual environment exists
    if [ ! -d "venv" ]; then
      echo -e "${YELLOW}Python virtual environment not found. Creating...${NC}"
      python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install backend dependencies
    cd code/backend
    pip install -r requirements.txt
    
    # Check if gunicorn is installed
    if ! command_exists gunicorn; then
      echo -e "${YELLOW}Gunicorn not found. Installing...${NC}"
      pip install gunicorn
    fi
    
    # Start backend services
    echo -e "${BLUE}Starting backend services with Gunicorn...${NC}"
    gunicorn main:app --workers 4 --bind 0.0.0.0:8000 --daemon
    
    cd ../..
    
    echo -e "${GREEN}Backend services deployed successfully.${NC}"
  fi
}

# Function to deploy frontend
deploy_frontend() {
  echo -e "\n${BLUE}Deploying frontend...${NC}"
  
  # Check if frontend directory exists
  if [ ! -d "code/frontend" ]; then
    echo -e "${RED}Error: Frontend directory not found.${NC}"
    echo -e "${YELLOW}Please ensure the frontend directory exists before proceeding.${NC}"
    exit 1
  fi
  
  # Check if we're deploying in Docker or directly
  if [ "$DEPLOY_MODE" = "docker" ]; then
    echo -e "${BLUE}Frontend is deployed via Docker.${NC}"
    echo -e "${BLUE}No additional action needed.${NC}"
  else
    echo -e "${BLUE}Building and deploying frontend directly...${NC}"
    
    # Check if Node.js is installed
    if ! command_exists node; then
      echo -e "${RED}Error: Node.js is not installed.${NC}"
      echo -e "${YELLOW}Please install Node.js before proceeding.${NC}"
      exit 1
    fi
    
    # Build frontend
    cd code/frontend
    npm install
    npm run build
    
    # Check if build directory exists
    if [ ! -d "build" ]; then
      echo -e "${RED}Error: Frontend build failed.${NC}"
      exit 1
    fi
    
    # Check if nginx is installed
    if ! command_exists nginx; then
      echo -e "${YELLOW}Nginx not found. Installing...${NC}"
      sudo apt-get update
      sudo apt-get install -y nginx
    fi
    
    # Deploy to nginx
    echo -e "${BLUE}Deploying frontend to Nginx...${NC}"
    sudo mkdir -p /var/www/quantumvest
    sudo cp -r build/* /var/www/quantumvest/
    
    # Create nginx configuration
    echo -e "${BLUE}Creating Nginx configuration...${NC}"
    sudo tee /etc/nginx/sites-available/quantumvest > /dev/null << EOL
server {
    listen 80;
    server_name _;
    
    root /var/www/quantumvest;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOL
    
    # Enable site and restart nginx
    sudo ln -sf /etc/nginx/sites-available/quantumvest /etc/nginx/sites-enabled/
    sudo nginx -t
    sudo systemctl restart nginx
    
    cd ../..
    
    echo -e "${GREEN}Frontend deployed successfully.${NC}"
  fi
}

# Function to deploy mobile frontend
deploy_mobile_frontend() {
  echo -e "\n${BLUE}Deploying mobile frontend...${NC}"
  
  # Check if mobile-frontend directory exists
  if [ ! -d "mobile-frontend" ]; then
    echo -e "${YELLOW}Mobile frontend directory not found. Skipping.${NC}"
    return
  fi
  
  echo -e "${BLUE}Building mobile frontend...${NC}"
  cd mobile-frontend
  npm install
  
  # Check if Expo is being used
  if grep -q "expo" package.json; then
    echo -e "${BLUE}Building Expo app...${NC}"
    
    # Check if expo-cli is installed
    if ! command_exists expo; then
      echo -e "${YELLOW}Expo CLI not found. Installing...${NC}"
      npm install -g expo-cli
    fi
    
    # Build for Android
    if [ "$BUILD_ANDROID" = "true" ]; then
      echo -e "${BLUE}Building for Android...${NC}"
      expo build:android -t apk
    fi
    
    # Build for iOS
    if [ "$BUILD_IOS" = "true" ]; then
      echo -e "${BLUE}Building for iOS...${NC}"
      expo build:ios -t archive
    fi
  else
    echo -e "${BLUE}Building React Native app...${NC}"
    
    # Check if React Native CLI is installed
    if ! command_exists react-native; then
      echo -e "${YELLOW}React Native CLI not found. Installing...${NC}"
      npm install -g react-native-cli
    fi
    
    # Build for Android
    if [ "$BUILD_ANDROID" = "true" ]; then
      echo -e "${BLUE}Building for Android...${NC}"
      cd android
      ./gradlew assembleRelease
      cd ..
    fi
    
    # Note: iOS builds require macOS
    if [ "$BUILD_IOS" = "true" ]; then
      echo -e "${YELLOW}iOS builds require macOS. Skipping.${NC}"
    fi
  fi
  
  cd ..
  
  echo -e "${GREEN}Mobile frontend build completed.${NC}"
  echo -e "${YELLOW}Note: You need to manually upload the built app to app stores.${NC}"
}

# Function to display help
show_help() {
  echo -e "${BLUE}Usage: $0 [options]${NC}"
  echo -e "${BLUE}Options:${NC}"
  echo -e "  ${GREEN}-h, --help${NC}                Show this help message"
  echo -e "  ${GREEN}-m, --mode <mode>${NC}         Deployment mode: docker (default) or direct"
  echo -e "  ${GREEN}-a, --android${NC}             Build for Android (mobile frontend only)"
  echo -e "  ${GREEN}-i, --ios${NC}                 Build for iOS (mobile frontend only)"
  echo -e "  ${GREEN}-s, --skip-database${NC}       Skip database initialization"
  echo -e "  ${GREEN}-f, --skip-frontend${NC}       Skip frontend deployment"
  echo -e "  ${GREEN}-b, --skip-backend${NC}        Skip backend deployment"
  echo -e "  ${GREEN}-m, --skip-mobile${NC}         Skip mobile frontend deployment"
}

# Main function
main() {
  # Default values
  DEPLOY_MODE="docker"
  BUILD_ANDROID="false"
  BUILD_IOS="false"
  SKIP_DATABASE="false"
  SKIP_FRONTEND="false"
  SKIP_BACKEND="false"
  SKIP_MOBILE="false"
  
  # Parse command line arguments
  while [ $# -gt 0 ]; do
    case "$1" in
      -h|--help)
        show_help
        exit 0
        ;;
      -m|--mode)
        DEPLOY_MODE="$2"
        shift
        ;;
      -a|--android)
        BUILD_ANDROID="true"
        ;;
      -i|--ios)
        BUILD_IOS="true"
        ;;
      -s|--skip-database)
        SKIP_DATABASE="true"
        ;;
      -f|--skip-frontend)
        SKIP_FRONTEND="true"
        ;;
      -b|--skip-backend)
        SKIP_BACKEND="true"
        ;;
      -m|--skip-mobile)
        SKIP_MOBILE="true"
        ;;
      *)
        echo -e "${RED}Unknown option: $1${NC}"
        show_help
        exit 1
        ;;
    esac
    shift
  done
  
  # Get the project directory
  PROJECT_DIR=$(pwd)
  
  echo -e "${BLUE}Project directory: $PROJECT_DIR${NC}"
  
  # Check if we're in the QuantumVest directory
  if [ ! -f "README.md" ] || ! grep -q "QuantumVest" "README.md"; then
    echo -e "${RED}Error: This doesn't appear to be the QuantumVest project directory.${NC}"
    echo -e "${YELLOW}Please run this script from the root of the QuantumVest project.${NC}"
    exit 1
  fi
  
  # Deploy Docker containers if in Docker mode
  if [ "$DEPLOY_MODE" = "docker" ]; then
    deploy_docker
  fi
  
  # Initialize database if not skipped
  if [ "$SKIP_DATABASE" = "false" ]; then
    initialize_database
  fi
  
  # Deploy backend if not skipped
  if [ "$SKIP_BACKEND" = "false" ]; then
    deploy_backend
  fi
  
  # Deploy frontend if not skipped
  if [ "$SKIP_FRONTEND" = "false" ]; then
    deploy_frontend
  fi
  
  # Deploy mobile frontend if not skipped
  if [ "$SKIP_MOBILE" = "false" ]; then
    deploy_mobile_frontend
  fi
  
  echo -e "\n${GREEN}QuantumVest deployment completed successfully!${NC}"
  
  # Print access information
  if [ "$DEPLOY_MODE" = "docker" ]; then
    echo -e "\n${BLUE}Access Information:${NC}"
    echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
    echo -e "${GREEN}Backend API:${NC} http://localhost:8000"
  else
    echo -e "\n${BLUE}Access Information:${NC}"
    echo -e "${GREEN}Frontend:${NC} http://localhost"
    echo -e "${GREEN}Backend API:${NC} http://localhost:8000"
  fi
}

# Run the main function with all arguments
main "$@"
