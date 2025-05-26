# QuantumVest Automation Scripts

This package contains a suite of automation scripts for the QuantumVest project. Below is documentation for each script, including purpose, usage, options, and key features.

---

## Scripts Overview

### 1. `env_setup.sh`

* **Purpose:** Automates the environment setup process for QuantumVest
* **Usage:**

  ```bash
  ./env_setup.sh
  ```
* **Features:**

  * Dependency checking and installation
  * Python and Node.js environment setup
  * Environment variable configuration
  * Database setup
  * Docker container initialization

---

### 2. `dev_workflow.sh`

* **Purpose:** Automates development workflow tasks
* **Usage:**

  ```bash
  ./dev_workflow.sh [options]
  ```
* **Options:**

  * `-h, --help`     Show help message
  * `-l, --lint`    Run linting only
  * `-t, --test`    Run tests only
  * `-q, --quality`   Run code quality checks only
  * `-d, --docs`    Generate documentation only
  * `-a, --all`     Run all checks (default)

---

### 3. `deploy.sh`

* **Purpose:** Automates the deployment process
* **Usage:**

  ```bash
  ./deploy.sh [options]
  ```
* **Options:**

  * `-h, --help`        Show help message
  * `-m, --mode <mode>`    Deployment mode: `docker` (default) or `direct`
  * `-a, --android`     Build for Android (mobile frontend only)
  * `-i, --ios`        Build for iOS (mobile frontend only)
  * `-s, --skip-database`    Skip database initialization
  * `-f, --skip-frontend`    Skip frontend deployment
  * `-b, --skip-backend`    Skip backend deployment
  * `-m, --skip-mobile`    Skip mobile frontend deployment

---

### 4. `maintenance.sh`

* **Purpose:** Automates maintenance tasks
* **Usage:**

  ```bash
  ./maintenance.sh [options]
  ```
* **Options:**

  * `-h, --help`     Show help message
  * `-l, --logs`     Rotate logs only
  * `-b, --backup`    Backup data only
  * `-c, --check`    Check system health only
  * `-a, --all`     Perform all maintenance tasks (default)

---

### 5. `cicd.sh`

* **Purpose:** Automates CI/CD processes
* **Usage:**

  ```bash
  ./cicd.sh [options]
  ```
* **Options:**

  * `-h, --help`        Show help message
  * `-g, --github-actions`   Set up GitHub Actions workflows only
  * `-r, --release`      Set up release management only
  * `-v, --version-control`   Set up version control hooks only
  * `-a, --all`     Set up all CI/CD enhancements (default)

---

## Installation Instructions

1. Extract the zip file into your QuantumVest project root directory.
2. Make all scripts executable:

   ```bash
   chmod +x *.sh
   ```
3. Run the scripts as needed based on the usage instructions above.

> **Note:** These scripts should be run from the root directory of the QuantumVest project. Each script will verify its execution directory before proceeding.