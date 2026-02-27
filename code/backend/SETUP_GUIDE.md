# QuantumVest Backend Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)
- 2GB+ free disk space

## Quick Start

### 1. Clone and Navigate

```bash
cd code/backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Note**: If you encounter space issues, install only essential dependencies first:

```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-CORS Flask-Caching
pip install PyJWT Werkzeug pandas numpy yfinance requests
pip install scikit-learn joblib cvxpy
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration (database, API keys, etc.)
```

### 5. Create Required Directories

```bash
mkdir -p ../resources/models
mkdir -p ../resources/data/stocks
mkdir -p ../resources/data/crypto
mkdir -p ../resources/data_cache
```

### 6. Initialize Database

```bash
export FLASK_APP=app.py
export FLASK_ENV=development

# Initialize database (creates tables)
python3 -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all(); print('Database initialized')"
```

### 7. Run the Application

**Option A: Using the run script (recommended)**

```bash
chmod +x run.sh
./run.sh
```

**Option B: Direct Python**

```bash
python3 app.py
```

The server will start on http://localhost:5000

## Verify Installation

### Health Check

```bash
curl http://localhost:5000/api/v1/health
```

Expected response:

```json
{
  "status": "healthy",
  "version": "2.0.0",
  "services": {
    "database": true,
    "prediction": true,
    "data_fetching": true,
    "storage": true
  }
}
```

### Register a Test User

```bash
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123!",
    "first_name": "Test",
    "last_name": "User"
  }'
```

## Configuration

### Database Options

**Development (SQLite - No setup required)**

```env
DATABASE_URL=sqlite:///quantumvest_dev.db
```

**Production (PostgreSQL)**

```env
DATABASE_URL=postgresql://user:password@localhost/quantumvest
```

### Optional Services

The backend will work without these, but some features will be limited:

- **Redis**: Caching and background tasks
- **External APIs**: Yahoo Finance (built-in), Alpha Vantage, CoinAPI
- **Email**: SMTP configuration for notifications

## Troubleshooting

### Import Errors

If you see module import errors, ensure all dependencies are installed:

```bash
pip list | grep -E "(Flask|pandas|numpy)"
```

### Database Errors

Reset the database:

```bash
rm -f quantumvest_dev.db
python3 -c "from app import create_app; app = create_app(); app.app_context().push(); from models import db; db.create_all()"
```

### Port Already in Use

Change the port in .env:

```env
PORT=8000
```

### Missing Directories

Run the directory creation commands from step 5 again.

## Development

### Running Tests

```bash
pytest tests/
```

### Database Migrations

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## API Documentation

Once running, access:

- API Endpoints: http://localhost:5000/api/v1/
- Health Check: http://localhost:5000/api/v1/health

### Main Endpoints

- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/portfolios` - Get user portfolios
- `POST /api/v1/portfolios` - Create portfolio
- `GET /api/v1/data/stocks/{symbol}` - Get stock data
- `GET /api/v1/data/crypto/{symbol}` - Get crypto data
- `GET /api/v1/predictions/stocks/{symbol}` - Get stock predictions

## Notes

- First startup will create default assets (major stocks and cryptos)
- ML models will be trained on-demand when predictions are requested
- Data is cached to improve performance
- The application uses SQLite by default for easy development

## Support

For issues or questions, refer to the main project documentation.
