#!/bin/bash
# QuantumVest Development Workflow Automation Script
# This script automates development workflow tasks including testing, linting, and code quality checks

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
echo -e "${GREEN}QuantumVest Development Workflow Automation Script${NC}"
echo -e "${BLUE}=================================================${NC}"

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Function to run linting on all code
run_linting() {
  echo -e "\n${BLUE}Running linting on all code...${NC}"

  # Check if lint-all.sh exists and use it if available
  if [ -f "lint-all.sh" ]; then
    echo -e "${BLUE}Using existing lint-all.sh script...${NC}"
    bash lint-all.sh
    return
  fi

  # Python linting
  if [ -d "code/backend" ] || [ -d "code/ai_models" ]; then
    echo -e "\n${BLUE}Running Python linting...${NC}"

    # Check if flake8 is installed
    if ! command_exists flake8; then
      echo -e "${YELLOW}flake8 not found. Installing...${NC}"
      pip install flake8
    fi

    # Check if black is installed
    if ! command_exists black; then
      echo -e "${YELLOW}black not found. Installing...${NC}"
      pip install black
    fi

    # Run flake8 on Python code
    echo -e "${BLUE}Running flake8...${NC}"
    find code -name "*.py" -exec flake8 {} \;

    # Run black on Python code
    echo -e "${BLUE}Running black...${NC}"
    find code -name "*.py" -exec black --check {} \;
  fi

  # JavaScript/TypeScript linting
  if [ -d "code/frontend" ] || [ -d "mobile-frontend" ] || [ -d "code/blockchain" ]; then
    echo -e "\n${BLUE}Running JavaScript/TypeScript linting...${NC}"

    # Frontend linting
    if [ -d "code/frontend" ]; then
      echo -e "${BLUE}Linting frontend code...${NC}"
      cd code/frontend

      # Check if package.json has lint script
      if grep -q "\"lint\":" package.json; then
        npm run lint
      else
        echo -e "${YELLOW}No lint script found in frontend package.json. Skipping.${NC}"
      fi

      cd ../..
    fi

    # Mobile frontend linting
    if [ -d "mobile-frontend" ]; then
      echo -e "${BLUE}Linting mobile frontend code...${NC}"
      cd mobile-frontend

      # Check if package.json has lint script
      if grep -q "\"lint\":" package.json; then
        npm run lint
      else
        echo -e "${YELLOW}No lint script found in mobile frontend package.json. Skipping.${NC}"
      fi

      cd ..
    fi

    # Blockchain linting
    if [ -d "code/blockchain" ]; then
      echo -e "${BLUE}Linting blockchain code...${NC}"
      cd code/blockchain

      # Check if package.json has lint script
      if grep -q "\"lint\":" package.json; then
        npm run lint
      else
        echo -e "${YELLOW}No lint script found in blockchain package.json. Skipping.${NC}"
      fi

      cd ../..
    fi
  fi

  # Terraform linting
  if [ -d "infrastructure" ] && find infrastructure -name "*.tf" -print -quit | grep -q .; then
    echo -e "\n${BLUE}Running Terraform linting...${NC}"

    # Check if tflint is installed
    if ! command_exists tflint; then
      echo -e "${YELLOW}tflint not found. Skipping Terraform linting.${NC}"
      echo -e "${YELLOW}Please install tflint for Terraform linting.${NC}"
    else
      cd infrastructure
      tflint
      cd ..
    fi
  fi

  echo -e "\n${GREEN}Linting completed.${NC}"
}

# Function to run tests
run_tests() {
  echo -e "\n${BLUE}Running tests...${NC}"

  # Backend tests
  if [ -d "code/backend" ]; then
    echo -e "\n${BLUE}Running backend tests...${NC}"
    cd code/backend

    # Check if pytest is installed
    if ! command_exists pytest; then
      echo -e "${YELLOW}pytest not found. Installing...${NC}"
      pip install pytest
    fi

    # Run pytest
    if [ -d "tests" ]; then
      pytest tests/
    else
      echo -e "${YELLOW}No tests directory found in backend. Skipping.${NC}"
    fi

    cd ../..
  fi

  # AI models tests
  if [ -d "code/ai_models" ]; then
    echo -e "\n${BLUE}Running AI models tests...${NC}"
    cd code/ai_models

    # Check if pytest is installed
    if ! command_exists pytest; then
      echo -e "${YELLOW}pytest not found. Installing...${NC}"
      pip install pytest
    fi

    # Run pytest
    if [ -d "tests" ]; then
      pytest tests/
    else
      echo -e "${YELLOW}No tests directory found in AI models. Skipping.${NC}"
    fi

    cd ../..
  fi

  # Frontend tests
  if [ -d "code/frontend" ]; then
    echo -e "\n${BLUE}Running frontend tests...${NC}"
    cd code/frontend

    # Check if package.json has test script
    if grep -q "\"test\":" package.json; then
      npm test -- --watchAll=false
    else
      echo -e "${YELLOW}No test script found in frontend package.json. Skipping.${NC}"
    fi

    cd ../..
  fi

  # Mobile frontend tests
  if [ -d "mobile-frontend" ]; then
    echo -e "\n${BLUE}Running mobile frontend tests...${NC}"
    cd mobile-frontend

    # Check if package.json has test script
    if grep -q "\"test\":" package.json; then
      npm test -- --watchAll=false
    else
      echo -e "${YELLOW}No test script found in mobile frontend package.json. Skipping.${NC}"
    fi

    cd ..
  fi

  # Blockchain tests
  if [ -d "code/blockchain" ]; then
    echo -e "\n${BLUE}Running blockchain tests...${NC}"
    cd code/blockchain

    # Check if package.json has test script
    if grep -q "\"test\":" package.json; then
      npm test
    else
      echo -e "${YELLOW}No test script found in blockchain package.json. Skipping.${NC}"
    fi

    cd ../..
  fi

  echo -e "\n${GREEN}Tests completed.${NC}"
}

# Function to run code quality checks
run_code_quality() {
  echo -e "\n${BLUE}Running code quality checks...${NC}"

  # Python code quality
  if [ -d "code/backend" ] || [ -d "code/ai_models" ]; then
    echo -e "\n${BLUE}Running Python code quality checks...${NC}"

    # Check if pylint is installed
    if ! command_exists pylint; then
      echo -e "${YELLOW}pylint not found. Installing...${NC}"
      pip install pylint
    fi

    # Run pylint on Python code
    echo -e "${BLUE}Running pylint...${NC}"
    find code -name "*.py" -exec pylint {} \; || true
  fi

  # JavaScript/TypeScript code quality
  if [ -d "code/frontend" ] || [ -d "mobile-frontend" ] || [ -d "code/blockchain" ]; then
    echo -e "\n${BLUE}Running JavaScript/TypeScript code quality checks...${NC}"

    # Check if eslint is installed
    if ! command_exists eslint; then
      echo -e "${YELLOW}eslint not found globally. Will use local installations if available.${NC}"
    fi

    # Frontend code quality
    if [ -d "code/frontend" ]; then
      echo -e "${BLUE}Checking frontend code quality...${NC}"
      cd code/frontend

      # Check if package.json has lint script
      if [ -f "node_modules/.bin/eslint" ]; then
        echo -e "${BLUE}Running ESLint...${NC}"
        ./node_modules/.bin/eslint src/ --max-warnings=0 || true
      fi

      cd ../..
    fi

    # Mobile frontend code quality
    if [ -d "mobile-frontend" ]; then
      echo -e "${BLUE}Checking mobile frontend code quality...${NC}"
      cd mobile-frontend

      # Check if package.json has lint script
      if [ -f "node_modules/.bin/eslint" ]; then
        echo -e "${BLUE}Running ESLint...${NC}"
        ./node_modules/.bin/eslint src/ --max-warnings=0 || true
      fi

      cd ..
    fi
  fi

  echo -e "\n${GREEN}Code quality checks completed.${NC}"
}

# Function to generate documentation
generate_docs() {
  echo -e "\n${BLUE}Generating documentation...${NC}"

  # Python documentation
  if [ -d "code/backend" ] || [ -d "code/ai_models" ]; then
    echo -e "\n${BLUE}Generating Python documentation...${NC}"

    # Check if sphinx is installed
    if ! command_exists sphinx-build; then
      echo -e "${YELLOW}sphinx not found. Installing...${NC}"
      pip install sphinx sphinx_rtd_theme
    fi

    # Create docs directory if it doesn't exist
    if [ ! -d "docs" ]; then
      mkdir -p docs
    fi

    # Generate backend documentation
    if [ -d "code/backend" ]; then
      echo -e "${BLUE}Generating backend documentation...${NC}"

      # Create backend docs directory if it doesn't exist
      if [ ! -d "docs/backend" ]; then
        mkdir -p docs/backend
        cd docs/backend
        sphinx-quickstart --no-sep -p "QuantumVest Backend" -a "QuantumVest Team" -v "1.0" -r "1.0" -l "en" --ext-autodoc --ext-viewcode --ext-todo
        cd ../..
      fi

      # Generate documentation
      cd docs/backend
      sphinx-build -b html . _build/html
      cd ../..

      echo -e "${GREEN}Backend documentation generated in docs/backend/_build/html${NC}"
    fi

    # Generate AI models documentation
    if [ -d "code/ai_models" ]; then
      echo -e "${BLUE}Generating AI models documentation...${NC}"

      # Create AI models docs directory if it doesn't exist
      if [ ! -d "docs/ai_models" ]; then
        mkdir -p docs/ai_models
        cd docs/ai_models
        sphinx-quickstart --no-sep -p "QuantumVest AI Models" -a "QuantumVest Team" -v "1.0" -r "1.0" -l "en" --ext-autodoc --ext-viewcode --ext-todo
        cd ../..
      fi

      # Generate documentation
      cd docs/ai_models
      sphinx-build -b html . _build/html
      cd ../..

      echo -e "${GREEN}AI models documentation generated in docs/ai_models/_build/html${NC}"
    fi
  fi

  # JavaScript/TypeScript documentation
  if [ -d "code/frontend" ] || [ -d "mobile-frontend" ] || [ -d "code/blockchain" ]; then
    echo -e "\n${BLUE}Generating JavaScript/TypeScript documentation...${NC}"

    # Frontend documentation
    if [ -d "code/frontend" ]; then
      echo -e "${BLUE}Generating frontend documentation...${NC}"
      cd code/frontend

      # Check if JSDoc is installed
      if [ -f "node_modules/.bin/jsdoc" ] || command_exists jsdoc; then
        # Create docs directory if it doesn't exist
        if [ ! -d "docs" ]; then
          mkdir -p docs
        fi

        # Use local JSDoc if available, otherwise use global
        if [ -f "node_modules/.bin/jsdoc" ]; then
          ./node_modules/.bin/jsdoc -r src -d docs
        else
          jsdoc -r src -d docs
        fi

        echo -e "${GREEN}Frontend documentation generated in code/frontend/docs${NC}"
      else
        echo -e "${YELLOW}JSDoc not found. Skipping frontend documentation generation.${NC}"
        echo -e "${YELLOW}Run 'npm install --save-dev jsdoc' to install JSDoc.${NC}"
      fi

      cd ../..
    fi
  fi

  echo -e "\n${GREEN}Documentation generation completed.${NC}"
}

# Function to display help
show_help() {
  echo -e "${BLUE}Usage: $0 [options]${NC}"
  echo -e "${BLUE}Options:${NC}"
  echo -e "  ${GREEN}-h, --help${NC}        Show this help message"
  echo -e "  ${GREEN}-l, --lint${NC}        Run linting only"
  echo -e "  ${GREEN}-t, --test${NC}        Run tests only"
  echo -e "  ${GREEN}-q, --quality${NC}     Run code quality checks only"
  echo -e "  ${GREEN}-d, --docs${NC}        Generate documentation only"
  echo -e "  ${GREEN}-a, --all${NC}         Run all checks (default)"
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
    # No arguments, run all checks
    run_linting
    run_tests
    run_code_quality
    generate_docs
  else
    while [ $# -gt 0 ]; do
      case "$1" in
        -h|--help)
          show_help
          exit 0
          ;;
        -l|--lint)
          run_linting
          ;;
        -t|--test)
          run_tests
          ;;
        -q|--quality)
          run_code_quality
          ;;
        -d|--docs)
          generate_docs
          ;;
        -a|--all)
          run_linting
          run_tests
          run_code_quality
          generate_docs
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

  echo -e "\n${GREEN}QuantumVest development workflow automation completed!${NC}"
}

# Run the main function with all arguments
main "$@"
