# GitHub Workflows Directory

This directory contains GitHub Actions workflows that automate the Continuous Integration and Continuous Deployment (CI/CD) pipeline for the QuantumVest project. These workflows help maintain code quality, run automated tests, and streamline the deployment process.

## Directory Structure

The `.github` directory is organized as follows:

```
.github/
└── workflows/
    └── ci-cd.yml
```

## Workflows

### CI/CD Pipeline (`ci-cd.yml`)

The CI/CD pipeline is configured to run automatically on push events to the main, master, and develop branches, as well as on pull requests targeting these branches. The workflow consists of three main jobs:

1. **Backend Testing**: This job runs on an Ubuntu environment and performs the following steps:
   - Sets up Python 3.10
   - Installs dependencies from the backend requirements file
   - Executes the backend test suite using pytest

2. **Frontend Testing**: This job also runs on an Ubuntu environment and performs the following steps:
   - Sets up Node.js 18
   - Installs frontend dependencies using npm
   - Runs the frontend test suite

3. **Build and Deploy**: This job only executes when code is pushed to the main or master branches (not on pull requests). It depends on the successful completion of both testing jobs and performs the following steps:
   - Sets up Node.js 18
   - Builds the frontend application
   - Sets up Python 3.10
   - Installs backend dependencies
   - Prepares for deployment (actual deployment steps would be customized based on your deployment strategy)

## Usage

The workflows in this directory run automatically based on the configured triggers. No manual intervention is required for normal operation. However, you can monitor the workflow execution in the "Actions" tab of the GitHub repository.

## Customization

To modify the CI/CD pipeline:

1. Edit the `ci-cd.yml` file to add, remove, or modify jobs and steps
2. Commit and push your changes to the repository
3. The updated workflow will be used for subsequent runs

For more complex workflows, you can add additional YAML files to the workflows directory.

## Best Practices

- Keep workflows focused on specific tasks
- Use GitHub secrets for sensitive information
- Cache dependencies to speed up workflow execution
- Use specific versions for actions to ensure stability

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
