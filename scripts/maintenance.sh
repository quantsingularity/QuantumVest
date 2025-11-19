#!/bin/bash
# QuantumVest Maintenance Automation Script
# This script automates maintenance tasks including log rotation, backups, and health monitoring

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
echo -e "${GREEN}QuantumVest Maintenance Automation Script${NC}"
echo -e "${BLUE}=================================================${NC}"

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to rotate logs
rotate_logs() {
  echo -e "\n${BLUE}Rotating logs...${NC}"

  # Create logs directory if it doesn't exist
  if [ ! -d "logs" ]; then
    mkdir -p logs
  fi

  # Check for log files in common locations
  LOG_FILES=(
    "code/backend/logs/*.log"
    "code/frontend/logs/*.log"
    "logs/*.log"
  )

  # Rotate each log file
  for pattern in "${LOG_FILES[@]}"; do
    for log_file in $pattern; do
      # Skip if the pattern doesn't match any files
      [ -e "$log_file" ] || continue

      echo -e "${BLUE}Rotating log file: $log_file${NC}"

      # Get base name of log file
      base_name=$(basename "$log_file")

      # Create timestamp
      timestamp=$(date +"%Y%m%d-%H%M%S")

      # Create archive directory if it doesn't exist
      archive_dir="logs/archive"
      mkdir -p "$archive_dir"

      # Copy log file to archive with timestamp
      cp "$log_file" "$archive_dir/${base_name%.*}-$timestamp.${base_name##*.}"

      # Clear original log file
      echo "" > "$log_file"
    done
  done

  # Compress logs older than 7 days
  echo -e "${BLUE}Compressing old logs...${NC}"
  find logs/archive -type f -name "*.log" -mtime +7 -exec gzip {} \;

  # Delete logs older than 30 days
  echo -e "${BLUE}Deleting logs older than 30 days...${NC}"
  find logs/archive -type f -name "*.gz" -mtime +30 -delete

  echo -e "${GREEN}Log rotation completed.${NC}"
}

# Function to backup data
backup_data() {
  echo -e "\n${BLUE}Backing up data...${NC}"

  # Create backup directory if it doesn't exist
  BACKUP_DIR="backups"
  mkdir -p "$BACKUP_DIR"

  # Create timestamp
  TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

  # Backup database
  echo -e "${BLUE}Backing up database...${NC}"

  # Extract database connection info from .env file
  if [ -f ".env" ]; then
    DB_URI=$(grep -oP 'DB_URI="\K[^"]*' .env)

    if [ -n "$DB_URI" ]; then
      # Parse DB_URI to extract components
      DB_USER=$(echo "$DB_URI" | grep -oP 'postgresql://\K[^:]*')
      DB_PASS=$(echo "$DB_URI" | grep -oP 'postgresql://[^:]*:\K[^@]*')
      DB_HOST=$(echo "$DB_URI" | grep -oP 'postgresql://[^:]*:[^@]*@\K[^:]*')
      DB_PORT=$(echo "$DB_URI" | grep -oP 'postgresql://[^:]*:[^@]*@[^:]*:\K[^/]*')
      DB_NAME=$(echo "$DB_URI" | grep -oP 'postgresql://[^:]*:[^@]*@[^:]*:[^/]*/\K[^"]*')

      # Backup database using pg_dump
      if command_exists pg_dump; then
        PGPASSWORD="$DB_PASS" pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$BACKUP_DIR/db-$TIMESTAMP.sql"

        # Compress the backup
        gzip "$BACKUP_DIR/db-$TIMESTAMP.sql"

        echo -e "${GREEN}Database backup completed: $BACKUP_DIR/db-$TIMESTAMP.sql.gz${NC}"
      else
        echo -e "${YELLOW}pg_dump not found. Skipping database backup.${NC}"
      fi
    else
      echo -e "${YELLOW}Could not extract database connection info from .env file.${NC}"
    fi
  else
    echo -e "${YELLOW}.env file not found. Skipping database backup.${NC}"
  fi

  # Backup code and configuration
  echo -e "${BLUE}Backing up code and configuration...${NC}"

  # Create a list of directories to backup
  BACKUP_DIRS=(
    "code"
    "docs"
    ".github"
    "infrastructure"
    "mobile-frontend"
  )

  # Create a list of files to backup
  BACKUP_FILES=(
    ".env"
    "docker-compose.yml"
    "README.md"
  )

  # Create a temporary directory for the backup
  TEMP_DIR=$(mktemp -d)

  # Copy directories
  for dir in "${BACKUP_DIRS[@]}"; do
    if [ -d "$dir" ]; then
      mkdir -p "$TEMP_DIR/$dir"
      cp -r "$dir" "$TEMP_DIR/$(dirname "$dir")"
    fi
  done

  # Copy files
  for file in "${BACKUP_FILES[@]}"; do
    if [ -f "$file" ]; then
      cp "$file" "$TEMP_DIR/$file"
    fi
  done

  # Create tar archive
  tar -czf "$BACKUP_DIR/code-$TIMESTAMP.tar.gz" -C "$TEMP_DIR" .

  # Remove temporary directory
  rm -rf "$TEMP_DIR"

  echo -e "${GREEN}Code and configuration backup completed: $BACKUP_DIR/code-$TIMESTAMP.tar.gz${NC}"

  # Delete backups older than 30 days
  echo -e "${BLUE}Deleting backups older than 30 days...${NC}"
  find "$BACKUP_DIR" -type f -name "*.gz" -mtime +30 -delete

  echo -e "${GREEN}Backup completed.${NC}"
}

# Function to check system health
check_health() {
  echo -e "\n${BLUE}Checking system health...${NC}"

  # Create health check directory if it doesn't exist
  HEALTH_DIR="health_checks"
  mkdir -p "$HEALTH_DIR"

  # Create timestamp
  TIMESTAMP=$(date +"%Y%m%d-%H%M%S")

  # Create health check report file
  HEALTH_REPORT="$HEALTH_DIR/health-$TIMESTAMP.txt"

  # Write header to health report
  echo "QuantumVest Health Check Report" > "$HEALTH_REPORT"
  echo "Date: $(date)" >> "$HEALTH_REPORT"
  echo "----------------------------------------" >> "$HEALTH_REPORT"

  # Check disk usage
  echo -e "${BLUE}Checking disk usage...${NC}"
  echo -e "\nDisk Usage:" >> "$HEALTH_REPORT"
  df -h >> "$HEALTH_REPORT"

  # Check memory usage
  echo -e "${BLUE}Checking memory usage...${NC}"
  echo -e "\nMemory Usage:" >> "$HEALTH_REPORT"
  free -h >> "$HEALTH_REPORT"

  # Check CPU usage
  echo -e "${BLUE}Checking CPU usage...${NC}"
  echo -e "\nCPU Usage:" >> "$HEALTH_REPORT"
  top -bn1 | head -20 >> "$HEALTH_REPORT"

  # Check running processes
  echo -e "${BLUE}Checking running processes...${NC}"
  echo -e "\nRunning Processes:" >> "$HEALTH_REPORT"
  ps aux | grep -E 'python|node|nginx|postgres|redis' | grep -v grep >> "$HEALTH_REPORT"

  # Check Docker containers if Docker is installed
  if command_exists docker; then
    echo -e "${BLUE}Checking Docker containers...${NC}"
    echo -e "\nDocker Containers:" >> "$HEALTH_REPORT"
    docker ps -a >> "$HEALTH_REPORT"
  fi

  # Check database connection
  echo -e "${BLUE}Checking database connection...${NC}"
  echo -e "\nDatabase Connection:" >> "$HEALTH_REPORT"

  # Extract database connection info from .env file
  if [ -f ".env" ]; then
    DB_URI=$(grep -oP 'DB_URI="\K[^"]*' .env)

    if [ -n "$DB_URI" ]; then
      # Parse DB_URI to extract components
      DB_USER=$(echo "$DB_URI" | grep -oP 'postgresql://\K[^:]*')
      DB_PASS=$(echo "$DB_URI" | grep -oP 'postgresql://[^:]*:\K[^@]*')
      DB_HOST=$(echo "$DB_URI" | grep -oP 'postgresql://[^:]*:[^@]*@\K[^:]*')
      DB_PORT=$(echo "$DB_URI" | grep -oP 'postgresql://[^:]*:[^@]*@[^:]*:\K[^/]*')
      DB_NAME=$(echo "$DB_URI" | grep -oP 'postgresql://[^:]*:[^@]*@[^:]*:[^/]*/\K[^"]*')

      # Check database connection
      if command_exists psql; then
        if PGPASSWORD="$DB_PASS" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1" > /dev/null 2>&1; then
          echo "Database connection successful." >> "$HEALTH_REPORT"
        else
          echo "Database connection failed." >> "$HEALTH_REPORT"
        fi
      else
        echo "psql not found. Could not check database connection." >> "$HEALTH_REPORT"
      fi
    else
      echo "Could not extract database connection info from .env file." >> "$HEALTH_REPORT"
    fi
  else
    echo ".env file not found. Could not check database connection." >> "$HEALTH_REPORT"
  fi

  # Check API endpoints
  echo -e "${BLUE}Checking API endpoints...${NC}"
  echo -e "\nAPI Endpoints:" >> "$HEALTH_REPORT"

  # Check if curl is installed
  if command_exists curl; then
    # Check backend API
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null | grep -q "200"; then
      echo "Backend API is up and running." >> "$HEALTH_REPORT"
    else
      echo "Backend API is not responding." >> "$HEALTH_REPORT"
    fi

    # Check frontend
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 2>/dev/null | grep -q "200"; then
      echo "Frontend is up and running." >> "$HEALTH_REPORT"
    else
      echo "Frontend is not responding." >> "$HEALTH_REPORT"
    fi
  else
    echo "curl not found. Could not check API endpoints." >> "$HEALTH_REPORT"
  fi

  echo -e "${GREEN}Health check completed. Report saved to $HEALTH_REPORT${NC}"

  # Display summary
  echo -e "\n${BLUE}Health Check Summary:${NC}"
  echo -e "${BLUE}----------------------------------------${NC}"

  # Check disk usage warning
  disk_usage=$(df -h | grep -E '/$' | awk '{print $5}' | sed 's/%//')
  if [ "$disk_usage" -gt 90 ]; then
    echo -e "${RED}WARNING: Disk usage is high ($disk_usage%).${NC}"
  else
    echo -e "${GREEN}Disk usage is normal ($disk_usage%).${NC}"
  fi

  # Check memory usage warning
  memory_usage=$(free | grep Mem | awk '{print int($3/$2 * 100)}')
  if [ "$memory_usage" -gt 90 ]; then
    echo -e "${RED}WARNING: Memory usage is high ($memory_usage%).${NC}"
  else
    echo -e "${GREEN}Memory usage is normal ($memory_usage%).${NC}"
  fi

  # Check if any critical services are down
  if grep -q "not responding\|failed\|not found" "$HEALTH_REPORT"; then
    echo -e "${RED}WARNING: Some services are not responding. Check the health report for details.${NC}"
  else
    echo -e "${GREEN}All services appear to be running normally.${NC}"
  fi
}

# Function to display help
show_help() {
  echo -e "${BLUE}Usage: $0 [options]${NC}"
  echo -e "${BLUE}Options:${NC}"
  echo -e "  ${GREEN}-h, --help${NC}        Show this help message"
  echo -e "  ${GREEN}-l, --logs${NC}        Rotate logs only"
  echo -e "  ${GREEN}-b, --backup${NC}      Backup data only"
  echo -e "  ${GREEN}-c, --check${NC}       Check system health only"
  echo -e "  ${GREEN}-a, --all${NC}         Perform all maintenance tasks (default)"
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

  # Parse command line arguments
  if [ $# -eq 0 ]; then
    # No arguments, perform all maintenance tasks
    rotate_logs
    backup_data
    check_health
  else
    while [ $# -gt 0 ]; do
      case "$1" in
        -h|--help)
          show_help
          exit 0
          ;;
        -l|--logs)
          rotate_logs
          ;;
        -b|--backup)
          backup_data
          ;;
        -c|--check)
          check_health
          ;;
        -a|--all)
          rotate_logs
          backup_data
          check_health
          ;;
        *)
          echo -e "${RED}Unknown option: $1${NC}"
          show_help
          exit 1
          ;;
      esac
      shift
    done
  fi

  echo -e "\n${GREEN}QuantumVest maintenance tasks completed!${NC}"
}

# Run the main function with all arguments
main "$@"
