#!/bin/bash
# Setup script for QuantumVest backend

set -e

echo "=== QuantumVest Backend Setup ==="
echo "Installing required packages..."

# Create virtual environment if needed
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install minimal dependencies for testing
pip install -q Flask Flask-SQLAlchemy Flask-CORS Flask-Migrate PyJWT Werkzeug bcrypt cryptography pandas numpy scikit-learn requests

echo ""
echo "=== Installation Complete ==="
echo ""
echo "To start the backend:"
echo "1. Set environment variables (optional):"
echo "   export FLASK_ENV=development"
echo "   export DATABASE_URL=sqlite:///quantumvest_dev.db"
echo ""
echo "2. Run the application:"
echo "   python3 app.py"
echo ""
