#!/bin/bash

# QuantumVest Project Setup Script (Comprehensive)

# Exit immediately if a command exits with a non-zero status.
set -e

# Prerequisites (ensure these are installed):
# - Python 3.x (the script will use python3.11 available in the environment)
# - pip (Python package installer)
# - Node.js (for frontend)
# - npm (Node package manager)
# - PostgreSQL (for backend database, as mentioned in README)
# - Access to blockchain data (Binance Smart Chain or Ethereum, as per README)
# - APIs for stock/crypto data (e.g., Alpha Vantage, CoinGecko, as per README)

echo "Starting QuantumVest project setup..."

PROJECT_DIR="/home/ubuntu/projects_extracted/QuantumVest"

if [ ! -d "${PROJECT_DIR}" ]; then
  echo "Error: Project directory ${PROJECT_DIR} not found."
  echo "Please ensure the project is extracted correctly."
  exit 1
fi

cd "${PROJECT_DIR}"
echo "Changed directory to $(pwd)"

# --- Backend Setup (Flask/Python) ---
echo ""
echo "Setting up QuantumVest Backend..."
BACKEND_DIR_QV="${PROJECT_DIR}/code/backend"

if [ ! -d "${BACKEND_DIR_QV}" ]; then
    echo "Error: Backend directory ${BACKEND_DIR_QV} not found. Skipping backend setup."
else
    cd "${BACKEND_DIR_QV}"
    echo "Changed directory to $(pwd) for backend setup."

    if [ ! -f "requirements.txt" ]; then
        echo "Error: requirements.txt not found in ${BACKEND_DIR_QV}. Cannot install backend dependencies."
    else
        echo "Creating Python virtual environment for backend (venv_quantumvest_backend_py)..."
        if ! python3.11 -m venv venv_quantumvest_backend_py; then
            echo "Failed to create backend virtual environment. Please check your Python installation."
        else
            source venv_quantumvest_backend_py/bin/activate
            echo "Backend Python virtual environment created and activated."
            
            echo "Installing backend Python dependencies from requirements.txt..."
            pip3 install -r requirements.txt
            echo "Backend dependencies installed."
            
            echo "To activate the backend virtual environment later, run: source ${BACKEND_DIR_QV}/venv_quantumvest_backend_py/bin/activate"
            echo "The README mentions Flask or FastAPI. Based on requirements.txt (flask), it is likely Flask."
            echo "To run the Flask backend, you would typically use a command like: flask run --host=0.0.0.0 --port=5000 (after setting FLASK_APP environment variable, e.g., export FLASK_APP=app.py)"
            echo "Please check the backend source code for the exact run command or app entry point."
            deactivate
            echo "Backend Python virtual environment deactivated."
        fi
    fi
    cd "${PROJECT_DIR}" # Return to the main project directory
fi

# --- Frontend Setup (React/Node.js) ---
echo ""
echo "Setting up QuantumVest Web Frontend..."
# README structure shows code/frontend, but package.json was found in code/web-frontend/
FRONTEND_DIR_QV="${PROJECT_DIR}/code/web-frontend"

if [ ! -d "${FRONTEND_DIR_QV}" ]; then
    # Fallback to code/frontend if code/web-frontend doesn't exist
    if [ -d "${PROJECT_DIR}/code/frontend" ]; then
        FRONTEND_DIR_QV="${PROJECT_DIR}/code/frontend"
        echo "Note: Using ${FRONTEND_DIR_QV} as web-frontend directory was not found."
    else
        echo "Error: Frontend directory (neither ${PROJECT_DIR}/code/web-frontend nor ${PROJECT_DIR}/code/frontend) not found. Skipping frontend setup."
        FRONTEND_DIR_QV=""
    fi
fi

if [ -n "${FRONTEND_DIR_QV}" ] && [ -d "${FRONTEND_DIR_QV}" ]; then
    cd "${FRONTEND_DIR_QV}"
    echo "Changed directory to $(pwd) for frontend setup."

    if [ ! -f "package.json" ]; then
        echo "Error: package.json not found in ${FRONTEND_DIR_QV}. Cannot install frontend dependencies."
    else
        echo "Installing frontend Node.js dependencies using npm..."
        if ! command -v npm &> /dev/null; then
            echo "npm command could not be found. Please ensure Node.js and npm are installed and in your PATH."
        else
            npm install
            echo "Frontend dependencies installed."
            echo "To start the frontend development server (from ${FRONTEND_DIR_QV}): npm start (or webpack serve --mode development --open as per package.json)"
            echo "To build the frontend for production (from ${FRONTEND_DIR_QV}): npm run build (or webpack --mode production as per package.json)"
        fi
    fi
    cd "${PROJECT_DIR}" # Return to the main project directory
fi

# --- AI Models & Blockchain components (Placeholder based on README structure) ---
echo ""
echo "Notes on other components mentioned in README (AI Models, Smart Contracts):"
AI_MODELS_DIR_QV="${PROJECT_DIR}/code/ai_models" # Assuming a similar structure if it exists
SMART_CONTRACTS_DIR_QV="${PROJECT_DIR}/code/smart_contracts" # Assuming a similar structure if it exists

if [ -d "${AI_MODELS_DIR_QV}" ]; then
    echo "- An 'ai_models' directory exists at ${AI_MODELS_DIR_QV}. Check for specific setup instructions or dependency files (e.g., requirements.txt) within it."
    if [ -f "${AI_MODELS_DIR_QV}/requirements.txt" ]; then
        echo "  Found requirements.txt in ${AI_MODELS_DIR_QV}. Consider setting up a separate Python environment for it."
    fi
elif [ -d "${PROJECT_DIR}/code" ]; then
    echo "- The 'code/' directory exists. AI models might be within subdirectories there. The README mentions Python (Scikit-learn, TensorFlow, PyTorch). Ensure these are installed in the relevant Python environment if used."
fi

if [ -d "${SMART_CONTRACTS_DIR_QV}" ]; then
    echo "- A 'smart_contracts' directory exists at ${SMART_CONTRACTS_DIR_QV}. Check for specific setup instructions or dependency files (e.g., package.json for Hardhat/Truffle, or Python requirements) within it."
    if [ -f "${SMART_CONTRACTS_DIR_QV}/package.json" ]; then
        echo "  Found package.json in ${SMART_CONTRACTS_DIR_QV}. It might be a Node.js based blockchain project (e.g., Hardhat, Truffle)."
    fi
elif [ -d "${PROJECT_DIR}/code" ]; then
    echo "- The 'code/' directory exists. Smart contracts might be within subdirectories there. The README mentions developing smart contracts."
fi

# --- Database Setup Reminder ---
echo ""
echo "Reminder: Ensure PostgreSQL is installed, running, and configured for the backend."
echo "Database connection details will likely be needed in the backend's environment or configuration."

# --- Data Collection Reminder ---
echo ""
echo "Reminder: Data Collection for AI Models."
echo "The README mentions gathering historical stock and crypto data from APIs like Alpha Vantage or CoinGecko."
echo "This will be a manual step or require separate scripts not covered by this environment setup."

echo ""
echo "QuantumVest project setup script finished."
echo "Please ensure all prerequisites (Python, Node.js, npm, PostgreSQL, API keys for data sources) are installed and configured."
echo "Review the project's README.md and the instructions above for running the backend and frontend."
echo "Manual setup will be required for AI Models and Blockchain components, including data collection and specific training/deployment steps."
