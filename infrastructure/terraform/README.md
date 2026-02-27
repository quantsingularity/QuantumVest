# QuantumVest Terraform Infrastructure

## Overview

This directory contains Terraform configurations for deploying QuantumVest infrastructure on AWS.

## Prerequisites

### Required Tools

```bash
# Terraform v1.5.0+
terraform --version

# AWS CLI v2
aws --version

# Optional: tflint for linting
tflint --version

# Optional: tfsec for security scanning
tfsec --version
```

### AWS Credentials

Configure AWS credentials using one of these methods:

```bash
# Method 1: AWS CLI
aws configure

# Method 2: Environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-west-2"

# Method 3: AWS Profile
export AWS_PROFILE="your-profile-name"
```

## Quick Start

### 1. Initialize Configuration

```bash
# Copy example configuration
cp terraform.tfvars.example terraform.tfvars

# Edit with your values
vi terraform.tfvars

# Set sensitive variables via environment
export TF_VAR_db_password="your-secure-password"
```

### 2. Initialize Terraform

```bash
# For local development (no remote state)
terraform init -backend=false

# OR with S3 backend (see backend-config.example)
cp backend-config.example backend.hcl
# Edit backend.hcl with your S3 bucket details
terraform init -backend-config=backend.hcl
```

### 3. Validate Configuration

```bash
# Format code
terraform fmt -recursive

# Validate syntax
terraform validate

# Run security checks (if tfsec installed)
tfsec .

# Lint (if tflint installed)
tflint --init
tflint
```

### 4. Plan Infrastructure

```bash
# Review changes
terraform plan -var-file="environments/dev/terraform.tfvars" -out=plan.out

# Or use specific environment
terraform plan -var-file="environments/prod/terraform.tfvars" -out=plan.out
```

### 5. Apply Infrastructure

```bash
# Apply changes
terraform apply plan.out

# Or apply directly (will prompt for confirmation)
terraform apply -var-file="environments/dev/terraform.tfvars"
```

### 6. Destroy Infrastructure (when needed)

```bash
terraform destroy -var-file="environments/dev/terraform.tfvars"
```

## Directory Structure

```
terraform/
├── main.tf                     # Main configuration
├── variables.tf                # Variable definitions
├── outputs.tf                  # Output definitions
├── terraform.tfvars.example    # Example configuration
├── backend-config.example      # Backend configuration example
├── environments/               # Environment-specific configs
│   ├── dev/
│   │   └── terraform.tfvars
│   ├── staging/
│   │   └── terraform.tfvars
│   └── prod/
│       └── terraform.tfvars
└── modules/                    # Reusable modules
    ├── compute/                # EC2, ASG, ALB
    ├── database/               # RDS
    ├── network/                # VPC, Subnets, IGW
    ├── security/               # Security Groups
    └── storage/                # S3 Buckets
```

## Modules

### Network Module

Creates VPC, subnets, internet gateway, NAT gateway, route tables.

- **Inputs**: vpc_cidr, availability_zones, subnet CIDRs
- **Outputs**: vpc_id, subnet_ids

### Compute Module

Creates EC2 instances, Auto Scaling Groups, Application Load Balancer.

- **Inputs**: instance_type, key_name, subnet_ids
- **Outputs**: instance_ids, lb_dns_name

### Database Module

Creates RDS instance with appropriate security and backup settings.

- **Inputs**: db_instance_class, db_name, credentials
- **Outputs**: db_endpoint, db_address

### Security Module

Creates security groups for application and database tiers.

- **Inputs**: vpc_id, allowed_cidrs
- **Outputs**: security_group_ids

### Storage Module

Creates S3 buckets for application data and backups.

- **Inputs**: app_name, environment
- **Outputs**: bucket_names, bucket_arns

## Environment Configuration

### Development

```bash
terraform apply -var-file="environments/dev/terraform.tfvars"
```

- Minimal resources
- No multi-AZ
- Short backup retention
- Cost-optimized

### Staging

```bash
terraform apply -var-file="environments/staging/terraform.tfvars"
```

- Production-like setup
- Multi-AZ optional
- Medium backup retention
- Testing ground

### Production

```bash
terraform apply -var-file="environments/prod/terraform.tfvars"
```

- High availability
- Multi-AZ enabled
- Extended backup retention
- Security hardened

## State Management

### Local State (Development)

```bash
# Initialize without backend
terraform init -backend=false

# State stored in: terraform.tfstate
```

### Remote State (Production)

```bash
# Setup S3 backend (one-time)
aws s3 mb s3://quantumvest-terraform-state
aws s3api put-bucket-versioning \
  --bucket quantumvest-terraform-state \
  --versioning-configuration Status=Enabled

# Create DynamoDB table for locking
aws dynamodb create-table \
  --table-name quantumvest-terraform-locks \
  --attribute-definitions AttributeName=LockID,AttributeType=S \
  --key-schema AttributeName=LockID,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

# Initialize with backend
terraform init -backend-config=backend.hcl
```

## Security Best Practices

### Secrets Management

1. **Never commit secrets** to version control
2. **Use environment variables** for sensitive values:
   ```bash
   export TF_VAR_db_password="secure-password"
   ```
3. **Use AWS Secrets Manager** in production:
   ```hcl
   data "aws_secretsmanager_secret_version" "db_password" {
     secret_id = "quantumvest/db/password"
   }
   ```

### State File Security

1. **Enable S3 bucket encryption**
2. **Enable S3 versioning** for state history
3. **Use DynamoDB** for state locking
4. **Restrict S3 bucket access** with IAM policies

### Resource Security

1. **Use security groups** to restrict access
2. **Enable encryption** at rest and in transit
3. **Use private subnets** for sensitive resources
4. **Enable AWS CloudTrail** for audit logging

## Common Commands

```bash
# Format all files
terraform fmt -recursive

# Validate configuration
terraform validate

# Show current state
terraform show

# List resources in state
terraform state list

# Show specific resource
terraform state show aws_instance.app

# Import existing resource
terraform import aws_instance.app i-1234567890abcdef0

# Refresh state
terraform refresh

# Target specific resource
terraform apply -target=module.network

# Generate dependency graph
terraform graph | dot -Tpng > graph.png
```

## Troubleshooting

### Issue: Backend initialization fails

```bash
# Solution: Check S3 bucket exists and you have permissions
aws s3 ls s3://quantumvest-terraform-state

# Re-initialize
terraform init -reconfigure
```

### Issue: State lock timeout

```bash
# Solution: Manually release lock (if stuck)
aws dynamodb delete-item \
  --table-name quantumvest-terraform-locks \
  --key '{"LockID": {"S": "quantumvest-terraform-state/dev/terraform.tfstate"}}'
```

### Issue: Provider authentication fails

```bash
# Solution: Verify AWS credentials
aws sts get-caller-identity

# Check environment variables
env | grep AWS
```

### Issue: Resource already exists

```bash
# Solution: Import existing resource
terraform import aws_vpc.main vpc-1234567890abcdef0
```

## Cost Estimation

```bash
# Install infracost
brew install infracost  # macOS
# OR
curl -fsSL https://raw.githubusercontent.com/infracost/infracost/master/scripts/install.sh | sh

# Estimate costs
infracost breakdown --path .

# Compare plan costs
terraform plan -out=plan.out
infracost breakdown --path plan.out
```

## Testing

### Validate locally

```bash
# Format check
terraform fmt -check -recursive

# Validate syntax
terraform validate

# Plan with mock variables
terraform plan -var-file="terraform.tfvars.example"
```

### Security scanning

```bash
# tfsec
tfsec . --minimum-severity MEDIUM

# Checkov
checkov -d . --framework terraform

# Terraform compliance
terraform-compliance -p plan.out -f compliance-tests/
```

## Maintenance

### Regular tasks

1. **Update provider versions** in required_providers
2. **Review and apply** security patches
3. **Test backup restoration** procedures
4. **Audit IAM permissions** regularly
5. **Clean up unused resources**

### State management

```bash
# Backup state before major changes
terraform state pull > backup.tfstate

# Clean up state (remove deleted resources)
terraform state rm aws_instance.old_instance
```
