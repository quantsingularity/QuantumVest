#!/bin/bash
# run_all_tests.sh: Runs all tests (frontend, backend, AI models, etc.) for QuantumVest.

# Exit immediately if a command exits with a non-zero status.
# Treat unset variables as an error.
# Exit if any command in a pipeline fails.
set -euo pipefail

# Define project root (assuming script is run from the project root or a known location)
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

echo "==================================================="
echo " Running All QuantumVest Tests"
echo "==================================================="

# --- Run Backend Tests ---
echo ""
echo "--- Running Backend Tests ---"
# Re-use the dedicated script for backend tests
"${PROJECT_DIR}/scripts/run_backend_tests.sh" || { echo "Error: Backend tests failed." >&2; exit 1; }

# --- Run Frontend Tests ---
echo ""
echo "--- Running Frontend Tests ---"
FRONTEND_DIR="${PROJECT_DIR}/code/web-frontend" # Assuming web-frontend is the correct path

if [ ! -d "${FRONTEND_DIR}" ]; then
    echo "Warning: Frontend directory not found at ${FRONTEND_DIR}. Skipping frontend tests."
else
    cd "${FRONTEND_DIR}"
    if ! command -v npm &> /dev/null; then
        echo "Error: npm command could not be found. Please ensure Node.js and npm are installed." >&2
    elif [ ! -f "package.json" ]; then
        echo "Error: package.json not found in ${FRONTEND_DIR}. Cannot run frontend tests." >&2
    else
        echo "Running 'npm test' for frontend..."
        # Note: 'npm test' often runs in watch mode. Using 'npm run test:ci' or similar is better for CI/CD.
        # Assuming 'npm test' is configured to run all tests and exit.
        npm test || { echo "Error: Frontend tests failed." >&2; cd "${PROJECT_DIR}"; exit 1; }
        echo "Frontend tests completed successfully."
    fi
    cd "${PROJECT_DIR}" # Return to the main project directory
fi

# --- Run AI Model Tests ---
echo ""
echo "--- Running AI Model Tests ---"
AI_MODELS_DIR="${PROJECT_DIR}/code/ai_models"

if [ ! -d "${AI_MODELS_DIR}" ]; then
    echo "Warning: AI Models directory not found at ${AI_MODELS_DIR}. Skipping AI model tests."
else
    cd "${AI_MODELS_DIR}"
    # Assuming tests are run using Python's built-in unittest module as per README suggestion
    echo "Running AI model tests with 'python -m unittest discover'..."
    python -m unittest discover || { echo "Error: AI model tests failed." >&2; cd "${PROJECT_DIR}"; exit 1; }
    echo "AI model tests completed successfully."
    cd "${PROJECT_DIR}" # Return to the main project directory
fi

# --- Run Blockchain Tests ---
echo ""
echo "--- Running Blockchain Tests ---"
BLOCKCHAIN_DIR="${PROJECT_DIR}/code/blockchain"

if [ ! -d "${BLOCKCHAIN_DIR}" ]; then
    echo "Warning: Blockchain directory not found at ${BLOCKCHAIN_DIR}. Skipping blockchain tests."
else
    cd "${BLOCKCHAIN_DIR}"
    if ! command -v npm &> /dev/null; then
        echo "Error: npm command could not be found. Please ensure Node.js and npm are installed." >&2
    elif [ ! -f "package.json" ]; then
        echo "Error: package.json not found in ${BLOCKCHAIN_DIR}. Cannot run blockchain tests." >&2
    else
        echo "Running 'npm test' for blockchain..."
        npm test || { echo "Error: Blockchain tests failed." >&2; cd "${PROJECT_DIR}"; exit 1; }
        echo "Blockchain tests completed successfully."
    fi
    cd "${PROJECT_DIR}" # Return to the main project directory
fi

echo ""
echo "==================================================="
echo " All QuantumVest tests finished successfully."
echo "==================================================="
