# QuantumVest CI/CD Pipeline

## Overview

GitHub Actions workflows for continuous integration and deployment of QuantumVest platform.

## Workflows

### Main Pipeline: `github-actions.yml`

Comprehensive CI/CD pipeline with multiple stages:

1. **Security Scanning** - Vulnerability and secret scanning
2. **Quality Gate** - Linting, testing, code analysis
3. **Build & Push** - Docker image building and publishing
4. **Infrastructure Validation** - Terraform, Kubernetes validation
5. **Deploy Staging** - Automated staging deployment
6. **Deploy Production** - Blue-green production deployment
7. **Compliance Audit** - Regulatory compliance checks
8. **Disaster Recovery Test** - Backup and recovery validation

## Required Secrets

### GitHub Secrets Configuration

Configure these secrets in GitHub repository settings (Settings → Secrets and variables → Actions):

#### AWS Credentials

```
AWS_ACCESS_KEY_ID          # AWS access key for staging
AWS_SECRET_ACCESS_KEY      # AWS secret key for staging
AWS_ACCESS_KEY_ID_PROD     # AWS access key for production
AWS_SECRET_ACCESS_KEY_PROD # AWS secret key for production
AWS_ACCESS_KEY_ID_DR       # AWS access key for DR testing
AWS_SECRET_ACCESS_KEY_DR   # AWS secret key for DR testing
```

#### Container Registry

```
GITHUB_TOKEN               # Automatically provided by GitHub Actions
                          # Used for ghcr.io authentication
```

#### Security Scanning

```
SNYK_TOKEN                # Snyk API token for vulnerability scanning
SONAR_TOKEN               # SonarCloud token for code quality
CODECOV_TOKEN             # Codecov token for coverage reporting
```

#### Notifications

```
SLACK_WEBHOOK_URL         # Slack webhook for deployment notifications
```

### Setting Up Secrets

```bash
# Using GitHub CLI
gh secret set AWS_ACCESS_KEY_ID --body "your-access-key-id"
gh secret set AWS_SECRET_ACCESS_KEY --body "your-secret-key"

# Or via GitHub UI
# Navigate to: Repository → Settings → Secrets and variables → Actions → New repository secret
```

## Local Testing

### Validate Workflow Syntax

```bash
# Install actionlint
# macOS: brew install actionlint
# Linux: https://github.com/rhysd/actionlint#installation

# Validate workflow
actionlint ci-cd/github-actions.yml

# Or use GitHub's workflow validation
gh workflow view
```

### Test with act

```bash
# Install act
# macOS: brew install act
# Linux: https://github.com/nektos/act#installation

# List workflows
act -l

# Run workflow locally (dry-run)
act -n

# Run specific job
act -j security-scan

# Run with secrets
act -s AWS_ACCESS_KEY_ID=test -s AWS_SECRET_ACCESS_KEY=test
```

## Required npm Scripts

The CI/CD pipeline expects these scripts in `package.json`:

```json
{
    "scripts": {
        "lint": "eslint . && prettier --check .",
        "test:unit": "jest --coverage",
        "test:integration": "jest --config jest.integration.config.js",
        "test:smoke": "jest --config jest.smoke.config.js",
        "test:security": "npm audit && snyk test",
        "test:health": "node scripts/health-check.js",
        "test:performance": "artillery run tests/performance.yml",
        "test:backup-restore": "node scripts/test-backup.js",
        "test:app-recovery": "node scripts/test-recovery.js",
        "test:data-integrity": "node scripts/test-integrity.js",
        "audit:sox": "node scripts/compliance/sox-audit.js",
        "audit:pci": "node scripts/compliance/pci-audit.js",
        "audit:gdpr": "node scripts/compliance/gdpr-audit.js",
        "audit:iso27001": "node scripts/compliance/iso27001-audit.js",
        "report:compliance": "node scripts/compliance/generate-report.js",
        "report:disaster-recovery": "node scripts/dr/generate-report.js"
    }
}
```

Create stub scripts if they don't exist:

```bash
mkdir -p scripts/compliance scripts/dr tests
touch scripts/health-check.js
touch scripts/test-backup.js
# ... etc
```

## Pipeline Stages

### 1. Security Scanning

**Triggers:** Every push, PR, daily schedule  
**Tools:**

- Trivy - Container vulnerability scanning
- Snyk - Dependency vulnerability scanning
- CodeQL - Static application security testing (SAST)
- GitLeaks - Secret scanning

```bash
# Run locally
docker run aquasec/trivy:latest fs .
snyk test
```

### 2. Quality Gate

**Triggers:** After security scan  
**Checks:**

- ESLint - Code linting
- Prettier - Code formatting
- Jest - Unit and integration tests
- SonarCloud - Code quality analysis
- Codecov - Test coverage

```bash
# Run locally
npm run lint
npm run test:unit
npm run test:integration
```

### 3. Build & Push

**Triggers:** After quality gate  
**Components:** backend, frontend, analytics
**Registry:** GitHub Container Registry (ghcr.io)

**Features:**

- Multi-architecture builds (amd64, arm64)
- BuildKit caching for faster builds
- Image signing with cosign
- SBOM generation

```bash
# Build locally
docker buildx build --platform linux/amd64,linux/arm64 \
  -t ghcr.io/quantumvest/backend:latest \
  -f backend/Dockerfile \
  backend/
```

### 4. Infrastructure Validation

**Triggers:** Every commit  
**Validations:**

- Terraform fmt, init, validate
- Kubernetes manifest validation (kubectl dry-run)
- Helm lint
- Checkov security scanning

```bash
# Run locally
cd infrastructure/terraform
terraform fmt -check -recursive
terraform init -backend=false
terraform validate

cd ../kubernetes
kubectl apply --dry-run=client -f base/

cd ../helm/quantumvest
helm lint .
```

### 5. Deploy Staging

**Triggers:** Push to `develop` branch  
**Environment:** staging.quantumvest.com  
**Steps:**

1. Configure kubectl
2. Deploy with Helm
3. Run smoke tests
4. Run security tests

```bash
# Manual staging deploy
helm upgrade --install quantumvest ./infrastructure/helm/quantumvest \
  --namespace quantumvest-staging \
  --create-namespace \
  --values ./infrastructure/helm/quantumvest/values-staging.yaml \
  --set image.tag=$(git rev-parse HEAD)
```

### 6. Deploy Production

**Triggers:** Push to `main` branch  
**Environment:** quantumvest.com  
**Strategy:** Blue-Green Deployment

**Steps:**

1. Pre-deployment validation
2. Deploy to green environment
3. Health checks on green
4. Switch traffic to green
5. Validate production
6. Cleanup blue environment

```bash
# Manual production deploy (blue-green)
# Deploy green
helm upgrade --install quantumvest-green ./infrastructure/helm/quantumvest \
  --namespace quantumvest-green \
  --create-namespace \
  --values ./infrastructure/helm/quantumvest/values-production.yaml \
  --set deployment.color=green

# After validation, switch traffic
kubectl patch ingress quantumvest-ingress -n quantumvest-production \
  --type merge \
  -p '{"spec":{"rules":[{"host":"quantumvest.com","http":{"paths":[{"path":"/","backend":{"service":{"name":"quantumvest-green"}}}]}}]}}'
```

### 7. Compliance Audit

**Triggers:** Daily schedule, manual with [audit] in commit message  
**Audits:**

- SOX (Sarbanes-Oxley)
- PCI DSS (Payment Card Industry)
- GDPR (Data Protection)
- ISO 27001 (Information Security)

**Retention:** 7 years for financial compliance

### 8. Disaster Recovery Test

**Triggers:** Daily schedule  
**Tests:**

- Database backup restoration
- Application recovery
- Data integrity validation

## Manual Workflow Triggers

### Trigger workflow manually

```bash
# Using GitHub CLI
gh workflow run "QuantumVest CI/CD Pipeline"

# Trigger specific workflow
gh workflow run github-actions.yml

# With inputs
gh workflow run github-actions.yml -f environment=staging
```

### Re-run failed workflow

```bash
gh run rerun <run-id>
gh run rerun <run-id> --failed
```

## Monitoring Workflows

### View workflow runs

```bash
# List recent runs
gh run list

# View specific run
gh run view <run-id>

# Watch run in real-time
gh run watch <run-id>

# View logs
gh run view <run-id> --log
```

### Check workflow status

```bash
# Check latest run status
gh run list --limit 1

# Check status of specific commit
gh run list --commit $(git rev-parse HEAD)
```

## Debugging Failed Workflows

### View logs

```bash
# Download logs
gh run download <run-id>

# View specific job logs
gh run view <run-id> --log --job <job-id>
```

### Debug with act

```bash
# Run failed job locally
act -j <job-name> -v

# With secrets
act -j <job-name> --secret-file .secrets
```

### Common Issues

#### Issue: Docker build fails

```bash
# Solution: Check Dockerfile syntax, build locally
docker build -t test ./backend/
```

#### Issue: Terraform validation fails

```bash
# Solution: Run terraform validate locally
cd infrastructure/terraform
terraform validate
```

#### Issue: Kubectl apply fails

```bash
# Solution: Validate manifests
kubectl apply --dry-run=client -f kubernetes/base/
```

#### Issue: Secrets not available

```bash
# Solution: Verify secrets are set
gh secret list

# Set missing secrets
gh secret set SECRET_NAME
```

## Branch Protection Rules

### Required for `main` branch:

- ✅ Require pull request reviews (2 approvals)
- ✅ Require status checks to pass:
    - security-scan
    - quality-gate
    - infrastructure-validation
- ✅ Require branches to be up to date
- ✅ Require conversation resolution
- ✅ Require signed commits
- ✅ Include administrators

### Required for `develop` branch:

- ✅ Require pull request reviews (1 approval)
- ✅ Require status checks to pass:
    - security-scan
    - quality-gate

## Deployment Approvals

### Staging Environment

- No approval required
- Auto-deploys on `develop` branch

### Production Environment

- Requires manual approval
- Configured in GitHub Environment settings
- Reviewers: DevOps team, Tech Lead

## Rollback Procedures

### Rollback staging

```bash
helm rollback quantumvest <revision> -n quantumvest-staging
```

### Rollback production (blue-green)

```bash
# Switch traffic back to blue
kubectl patch ingress quantumvest-ingress -n quantumvest-production \
  --type merge \
  -p '{"spec":{"rules":[{"host":"quantumvest.com","http":{"paths":[{"path":"/","backend":{"service":{"name":"quantumvest-blue"}}}]}}]}}'

# Or use Helm
helm rollback quantumvest-green <revision> -n quantumvest-green
```

## Best Practices

### 1. Small, Frequent Commits

- Push code frequently
- Keep PRs focused and small
- Fix failing tests immediately

### 2. Use Feature Flags

- Deploy code disabled
- Enable features incrementally
- A/B test in production

### 3. Monitor Deployments

- Watch metrics during deployment
- Set up alerts for anomalies
- Have rollback plan ready

### 4. Test Before Merge

- Run tests locally
- Use pre-commit hooks
- Review pipeline results

### 5. Secure Secrets

- Never commit secrets
- Rotate secrets regularly
- Use least privilege access

## Performance Optimization

### Speed up builds

```yaml
# Use caching
- uses: actions/cache@v3
  with:
      path: ~/.npm
      key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}

# Use BuildKit cache
- uses: docker/build-push-action@v5
  with:
      cache-from: type=gha
      cache-to: type=gha,mode=max
```

### Parallel jobs

```yaml
# Run independent jobs in parallel
jobs:
    test-unit:
        # runs in parallel with test-integration
    test-integration:
        # runs in parallel with test-unit
```

## Cost Optimization

### GitHub Actions minutes

- Use self-hosted runners for heavy workloads
- Cache dependencies aggressively
- Skip unnecessary jobs with conditions
- Use matrix strategies efficiently

```yaml
# Skip CI on docs-only changes
if: "!contains(github.event.head_commit.message, '[skip ci]')"

# Only run on specific paths
paths:
    - 'src/**'
    - 'tests/**'
    - '!docs/**'
```
