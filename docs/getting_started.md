# Getting Started with QuantumVest

This guide will help you set up and run the Predictive Investment Analytics Platform (QuantumVest) on your local environment.

## Prerequisites

Before installing QuantumVest, ensure you have the following prerequisites installed:

- **Python 3.8+** - For backend and AI model execution
- **Node.js 14+** - For frontend development
- **Docker** - For containerized deployment
- **Docker Compose** - For multi-container applications
- **Git** - For version control
- **PostgreSQL 13+** - For database operations
- **Truffle Suite** - For blockchain development

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-organization/quantumvest.git
cd quantumvest
```

### 2. Backend Setup

Navigate to the backend directory and set up a Python virtual environment:

```bash
cd code/backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Configure the environment variables by copying the example file:

```bash
cp .env.example .env
```

Edit the `.env` file to include your database credentials and API keys.

### 3. Frontend Setup

Navigate to the frontend directory and install dependencies:

```bash
cd ../frontend
npm install
```

Configure the frontend environment variables:

```bash
cp .env.example .env
```

Edit the `.env` file to include your backend API URL and other configuration.

### 4. Database Setup

Create a PostgreSQL database for the application:

```bash
createdb quantumvest
```

Run the database migrations:

```bash
cd ../backend
python manage.py db upgrade
```

### 5. Blockchain Setup

Navigate to the blockchain directory and install dependencies:

```bash
cd ../blockchain
npm install
```

Compile and deploy the smart contracts:

```bash
truffle compile
truffle migrate --network development
```

### 6. AI Models Setup

Navigate to the AI models directory:

```bash
cd ../ai_models
```

The pre-trained models are included in the repository. If you want to retrain them:

```bash
cd training_scripts
python train_prediction_model.py
python train_optimization_model.py
```

## Running the Application

### 1. Start the Backend Server

```bash
cd ../../backend
python app.py
```

The backend server will start at http://localhost:5000.

### 2. Start the Frontend Development Server

```bash
cd ../frontend
npm start
```

The frontend development server will start at http://localhost:3000.

### 3. Access the Application

Open your browser and navigate to http://localhost:3000 to access the QuantumVest application.

## Docker Deployment

For a containerized deployment, you can use Docker Compose:

```bash
cd ../../
docker-compose up -d
```

This will start all the necessary services (backend, frontend, database) in containers.

## Kubernetes Deployment

For production deployment using Kubernetes:

```bash
cd infrastructure/kubernetes
kubectl apply -f base/
```

## Troubleshooting

If you encounter any issues during installation or running the application, please check the following:

1. Ensure all prerequisites are installed and properly configured
2. Verify that all environment variables are correctly set
3. Check the logs for any error messages
4. Make sure the database is running and accessible
5. Ensure the required ports are not being used by other applications

For more detailed troubleshooting, refer to the [Technical Documentation](./technical_documentation.md).

## Next Steps

Once you have the application running, you can:

- Create an account and explore the platform
- Check out the [User Manual](./user_manual.md) for detailed usage instructions
- Refer to the [API Documentation](./api_documentation.md) if you want to integrate with the platform
- Explore the [Developer Guide](./developer_guide.md) if you want to contribute to the project
