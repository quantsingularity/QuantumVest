# Infrastructure Guide

## Overview

This guide provides comprehensive information about the infrastructure setup for the QuantumVest platform. It covers the deployment architecture, Kubernetes configuration, Terraform infrastructure, and Ansible automation.

## Deployment Architecture

QuantumVest uses a cloud-native architecture deployed across multiple environments (development, staging, and production). The infrastructure is designed to be scalable, resilient, and secure.

### Environment Architecture

![Deployment Architecture](../resources/designs/deployment_architecture.png)

The platform is deployed across three environments:

1. **Development Environment**
   - Purpose: Feature development and testing
   - Scale: Minimal resources for cost efficiency
   - Data: Synthetic test data
   - Access: Internal team only

2. **Staging Environment**
   - Purpose: Pre-production testing and QA
   - Scale: Similar to production but smaller
   - Data: Anonymized production data
   - Access: Internal team and selected beta testers

3. **Production Environment**
   - Purpose: Live application serving end users
   - Scale: Full scale with auto-scaling enabled
   - Data: Real user and market data
   - Access: Public users and administrators

### Component Architecture

The infrastructure consists of the following main components:

1. **Compute Layer**
   - Kubernetes clusters for container orchestration
   - Managed node groups with auto-scaling
   - Spot instances for cost optimization (non-critical workloads)

2. **Database Layer**
   - Primary PostgreSQL database for transactional data
   - Read replicas for scaling read operations
   - Automated backups and point-in-time recovery

3. **Caching Layer**
   - Redis clusters for caching and session management
   - Multi-AZ deployment for high availability

4. **Storage Layer**
   - Object storage for static assets and backups
   - Block storage for persistent volumes
   - File storage for shared data

5. **Networking Layer**
   - Virtual private cloud with public and private subnets
   - Load balancers for traffic distribution
   - Content delivery network for static assets
   - VPN for secure administrative access

6. **Security Layer**
   - Web application firewall
   - DDoS protection
   - Network ACLs and security groups
   - Encryption for data at rest and in transit

7. **Monitoring Layer**
   - Metrics collection and visualization
   - Log aggregation and analysis
   - Alerting and notification system
   - Performance monitoring

## Kubernetes Configuration

QuantumVest uses Kubernetes for container orchestration. The Kubernetes configuration is organized as follows:

```
infrastructure/kubernetes/
├── base/                       # Base Kubernetes manifests
│   ├── app-configmap.yaml      # Application configuration
│   ├── app-secrets.yaml        # Application secrets
│   ├── backend-deployment.yaml # Backend deployment
│   ├── backend-service.yaml    # Backend service
│   ├── database-service.yaml   # Database service
│   ├── database-statefulset.yaml # Database stateful set
│   ├── frontend-deployment.yaml # Frontend deployment
│   ├── frontend-service.yaml   # Frontend service
│   ├── ingress.yaml            # Ingress configuration
│   ├── redis-deployment.yaml   # Redis deployment
│   ├── redis-pvc.yaml          # Redis persistent volume claim
│   └── redis-service.yaml      # Redis service
└── environments/               # Environment-specific configurations
    ├── dev/                    # Development environment
    │   └── values.yaml         # Development values
    ├── staging/                # Staging environment
    │   └── values.yaml         # Staging values
    └── prod/                   # Production environment
        └── values.yaml         # Production values
```

### Key Kubernetes Components

#### Backend Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
        - name: backend
          image: quantumvest/backend:latest
          ports:
            - containerPort: 5000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
          resources:
            requests:
              memory: "256Mi"
              cpu: "100m"
            limits:
              memory: "512Mi"
              cpu: "500m"
          livenessProbe:
            httpGet:
              path: /health
              port: 5000
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /ready
              port: 5000
            initialDelaySeconds: 5
            periodSeconds: 5
```

#### Frontend Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
        - name: frontend
          image: quantumvest/frontend:latest
          ports:
            - containerPort: 80
          env:
            - name: API_URL
              valueFrom:
                configMapKeyRef:
                  name: app-configmap
                  key: api-url
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "300m"
          livenessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 30
            periodSeconds: 10
          readinessProbe:
            httpGet:
              path: /
              port: 80
            initialDelaySeconds: 5
            periodSeconds: 5
```

#### Ingress Configuration

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: quantumvest-ingress
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts:
        - api.quantumvest.com
        - www.quantumvest.com
      secretName: quantumvest-tls
  rules:
    - host: api.quantumvest.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: backend
                port:
                  number: 5000
    - host: www.quantumvest.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 80
```

### Deploying to Kubernetes

To deploy the application to Kubernetes:

1. Set up kubectl to point to your cluster:

```bash
aws eks update-kubeconfig --name quantumvest-cluster --region us-west-2
```

2. Apply the base configurations:

```bash
kubectl apply -f infrastructure/kubernetes/base/
```

3. Apply environment-specific configurations:

```bash
# For development
kubectl apply -f infrastructure/kubernetes/environments/dev/

# For staging
kubectl apply -f infrastructure/kubernetes/environments/staging/

# For production
kubectl apply -f infrastructure/kubernetes/environments/prod/
```

4. Verify the deployments:

```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

## Terraform Infrastructure

QuantumVest uses Terraform for infrastructure as code. The Terraform configuration is organized as follows:

```
infrastructure/terraform/
├── main.tf                 # Main Terraform configuration
├── variables.tf            # Input variables
├── outputs.tf              # Output values
├── environments/           # Environment-specific configurations
│   ├── dev/                # Development environment
│   │   └── terraform.tfvars # Development variables
│   ├── staging/            # Staging environment
│   │   └── terraform.tfvars # Staging variables
│   └── prod/               # Production environment
│       └── terraform.tfvars # Production variables
└── modules/                # Reusable Terraform modules
    ├── compute/            # Compute resources (EKS, EC2)
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    ├── database/           # Database resources (RDS)
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    ├── network/            # Network resources (VPC, subnets)
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    ├── security/           # Security resources (IAM, WAF)
    │   ├── main.tf
    │   ├── variables.tf
    │   └── outputs.tf
    └── storage/            # Storage resources (S3, EBS)
        ├── main.tf
        ├── variables.tf
        └── outputs.tf
```

### Key Terraform Modules

#### Network Module

```hcl
# modules/network/main.tf

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "${var.environment}-vpc"
    Environment = var.environment
  }
}

resource "aws_subnet" "public" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.public_subnet_cidrs[count.index]
  availability_zone       = var.availability_zones[count.index]
  map_public_ip_on_launch = true

  tags = {
    Name        = "${var.environment}-public-subnet-${count.index + 1}"
    Environment = var.environment
    Type        = "Public"
  }
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]

  tags = {
    Name        = "${var.environment}-private-subnet-${count.index + 1}"
    Environment = var.environment
    Type        = "Private"
  }
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name        = "${var.environment}-igw"
    Environment = var.environment
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name        = "${var.environment}-public-route-table"
    Environment = var.environment
  }
}

resource "aws_route_table_association" "public" {
  count          = length(var.public_subnet_cidrs)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}
```

#### Compute Module

```hcl
# modules/compute/main.tf

resource "aws_eks_cluster" "main" {
  name     = "${var.environment}-eks-cluster"
  role_arn = aws_iam_role.eks_cluster.arn
  version  = var.kubernetes_version

  vpc_config {
    subnet_ids              = var.subnet_ids
    endpoint_private_access = true
    endpoint_public_access  = true
    security_group_ids      = [aws_security_group.eks_cluster.id]
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy,
    aws_iam_role_policy_attachment.eks_service_policy,
  ]

  tags = {
    Name        = "${var.environment}-eks-cluster"
    Environment = var.environment
  }
}

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.environment}-node-group"
  node_role_arn   = aws_iam_role.eks_nodes.arn
  subnet_ids      = var.subnet_ids
  instance_types  = var.instance_types
  disk_size       = var.disk_size

  scaling_config {
    desired_size = var.desired_capacity
    max_size     = var.max_size
    min_size     = var.min_size
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.ecr_read_only,
  ]

  tags = {
    Name        = "${var.environment}-node-group"
    Environment = var.environment
  }
}
```

#### Database Module

```hcl
# modules/database/main.tf

resource "aws_db_subnet_group" "main" {
  name       = "${var.environment}-db-subnet-group"
  subnet_ids = var.subnet_ids

  tags = {
    Name        = "${var.environment}-db-subnet-group"
    Environment = var.environment
  }
}

resource "aws_db_instance" "main" {
  identifier             = "${var.environment}-db"
  engine                 = "postgres"
  engine_version         = var.postgres_version
  instance_class         = var.instance_class
  allocated_storage      = var.allocated_storage
  storage_type           = "gp2"
  storage_encrypted      = true
  db_name                = var.db_name
  username               = var.db_username
  password               = var.db_password
  vpc_security_group_ids = [aws_security_group.db.id]
  db_subnet_group_name   = aws_db_subnet_group.main.name
  parameter_group_name   = aws_db_parameter_group.main.name
  publicly_accessible    = false
  skip_final_snapshot    = var.environment != "prod"
  backup_retention_period = var.environment == "prod" ? 7 : 1
  backup_window           = "03:00-04:00"
  maintenance_window      = "Mon:04:00-Mon:05:00"
  multi_az                = var.environment == "prod"

  tags = {
    Name        = "${var.environment}-db"
    Environment = var.environment
  }
}

resource "aws_db_parameter_group" "main" {
  name   = "${var.environment}-db-parameter-group"
  family = "postgres13"

  parameter {
    name  = "log_connections"
    value = "1"
  }

  parameter {
    name  = "log_disconnections"
    value = "1"
  }

  tags = {
    Name        = "${var.environment}-db-parameter-group"
    Environment = var.environment
  }
}
```

### Deploying with Terraform

To deploy the infrastructure with Terraform:

1. Initialize Terraform:

```bash
cd infrastructure/terraform
terraform init
```

2. Select the appropriate environment:

```bash
# For development
terraform workspace select dev
terraform plan -var-file=environments/dev/terraform.tfvars

# For staging
terraform workspace select staging
terraform plan -var-file=environments/staging/terraform.tfvars

# For production
terraform workspace select prod
terraform plan -var-file=environments/prod/terraform.tfvars
```

3. Apply the configuration:

```bash
terraform apply -var-file=environments/[environment]/terraform.tfvars
```

4. Verify the deployment:

```bash
terraform output
```

## Ansible Automation

QuantumVest uses Ansible for configuration management and automation. The Ansible configuration is organized as follows:

```
infrastructure/ansible/
├── inventory/              # Inventory files
│   └── hosts.yml           # Host definitions
├── playbooks/              # Ansible playbooks
│   └── main.yml            # Main playbook
└── roles/                  # Ansible roles
    ├── common/             # Common configuration
    │   └── tasks/
    │       └── main.yml
    ├── database/           # Database configuration
    │   ├── handlers/
    │   │   └── main.yml
    │   ├── tasks/
    │   │   └── main.yml
    │   ├── templates/
    │   │   └── my.cnf.j2
    │   └── vars/
    │       └── main.yml
    └── webserver/          # Web server configuration
        ├── handlers/
        │   └── main.yml
        ├── tasks/
        │   └── main.yml
        ├── templates/
        │   └── nginx.conf.j2
        └── vars/
            └── main.yml
```

### Key Ansible Roles

#### Common Role

```yaml
# roles/common/tasks/main.yml

- name: Update apt cache
  apt:
    update_cache: yes
    cache_valid_time: 3600
  become: yes

- name: Install common packages
  apt:
    name:
      - curl
      - vim
      - git
      - htop
      - unzip
      - python3-pip
      - python3-venv
      - ntp
    state: present
  become: yes

- name: Set timezone
  timezone:
    name: UTC
  become: yes

- name: Configure NTP
  service:
    name: ntp
    state: started
    enabled: yes
  become: yes

- name: Create application directory
  file:
    path: /opt/quantumvest
    state: directory
    owner: "{{ app_user }}"
    group: "{{ app_group }}"
    mode: "0755"
  become: yes
```

#### Webserver Role

```yaml
# roles/webserver/tasks/main.yml

- name: Install Nginx
  apt:
    name: nginx
    state: present
  become: yes
  notify: restart nginx

- name: Configure Nginx
  template:
    src: nginx.conf.j2
    dest: /etc/nginx/nginx.conf
    owner: root
    group: root
    mode: "0644"
  become: yes
  notify: restart nginx

- name: Create Nginx server block
  template:
    src: vhost.conf.j2
    dest: /etc/nginx/sites-available/quantumvest
    owner: root
    group: root
    mode: "0644"
  become: yes
  notify: restart nginx

- name: Enable Nginx server block
  file:
    src: /etc/nginx/sites-available/quantumvest
    dest: /etc/nginx/sites-enabled/quantumvest
    state: link
  become: yes
  notify: restart nginx

- name: Remove default Nginx server block
  file:
    path: /etc/nginx/sites-enabled/default
    state: absent
  become: yes
  notify: restart nginx
```

#### Database Role

```yaml
# roles/database/tasks/main.yml

- name: Install PostgreSQL
  apt:
    name:
      - postgresql
      - postgresql-contrib
      - python3-psycopg2
    state: present
  become: yes

- name: Configure PostgreSQL
  template:
    src: postgresql.conf.j2
    dest: /etc/postgresql/13/main/postgresql.conf
    owner: postgres
    group: postgres
    mode: "0644"
  become: yes
  notify: restart postgresql

- name: Configure PostgreSQL client authentication
  template:
    src: pg_hba.conf.j2
    dest: /etc/postgresql/13/main/pg_hba.conf
    owner: postgres
    group: postgres
    mode: "0640"
  become: yes
  notify: restart postgresql

- name: Ensure PostgreSQL is running
  service:
    name: postgresql
    state: started
    enabled: yes
  become: yes

- name: Create PostgreSQL database
  postgresql_db:
    name: "{{ db_name }}"
    encoding: UTF-8
    lc_collate: en_US.UTF-8
    lc_ctype: en_US.UTF-8
    template: template0
  become: yes
  become_user: postgres

- name: Create PostgreSQL user
  postgresql_user:
    name: "{{ db_user }}"
    password: "{{ db_password }}"
    role_attr_flags: CREATEDB,NOSUPERUSER
  become: yes
  become_user: postgres

- name: Grant privileges on database
  postgresql_privs:
    db: "{{ db_name }}"
    role: "{{ db_user }}"
    type: database
    privs: ALL
  become: yes
  become_user: postgres
```

### Running Ansible Playbooks

To run Ansible playbooks:

1. Ensure your inventory is up to date:

```bash
cd infrastructure/ansible
```

2. Run the main playbook:

```bash
ansible-playbook -i inventory/hosts.yml playbooks/main.yml
```

3. Run a specific role:

```bash
ansible-playbook -i inventory/hosts.yml playbooks/main.yml --tags "webserver"
```

## Monitoring and Logging

QuantumVest uses a comprehensive monitoring and logging stack:

### Monitoring Stack

- **Prometheus**: Metrics collection and storage
- **Grafana**: Metrics visualization and dashboards
- **Alertmanager**: Alert routing and notifications

### Logging Stack

- **Elasticsearch**: Log storage and indexing
- **Logstash**: Log processing and transformation
- **Kibana**: Log visualization and analysis
- **Filebeat**: Log shipping from applications

### Key Metrics to Monitor

1. **System Metrics**
   - CPU usage
   - Memory usage
   - Disk space
   - Network traffic

2. **Application Metrics**
   - Request rate
   - Error rate
   - Response time
   - Active users

3. **Database Metrics**
   - Query performance
   - Connection count
   - Transaction rate
   - Cache hit ratio

4. **Kubernetes Metrics**
   - Pod status
   - Node health
   - Resource utilization
   - Deployment status

### Alerting Rules

Configure alerting rules in Prometheus for critical conditions:

```yaml
groups:
  - name: example
    rules:
      - alert: HighCPUUsage
        expr: avg(node_cpu_seconds_total{mode="idle"}) by (instance) < 0.2
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High CPU usage on {{ $labels.instance }}
          description: CPU usage is above 80% for more than 5 minutes.

      - alert: HighMemoryUsage
        expr: node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes * 100 < 10
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: High memory usage on {{ $labels.instance }}
          description: Memory available is less than 10% for more than 5 minutes.

      - alert: HighAPIErrorRate
        expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100 > 5
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: High API error rate
          description: API error rate is above 5% for more than 5 minutes.
```

## Backup and Disaster Recovery

QuantumVest implements a comprehensive backup and disaster recovery strategy:

### Database Backups

- **Automated daily backups**: Full database dumps stored in object storage
- **Point-in-time recovery**: Transaction logs for granular recovery
- **Cross-region replication**: Backups replicated to secondary region

### Application State

- **Configuration backups**: Infrastructure as code stored in version control
- **Stateful data**: Persistent volumes backed up regularly
- **Secrets management**: Encrypted secrets with versioning

### Disaster Recovery Plan

1. **RTO (Recovery Time Objective)**: 1 hour for critical systems
2. **RPO (Recovery Point Objective)**: 15 minutes for database
3. **Failover procedure**:
   - Activate standby database in secondary region
   - Redirect traffic to backup infrastructure
   - Restore application state from backups
4. **Regular testing**: Monthly DR drills to validate procedures

## Security Considerations

QuantumVest prioritizes security throughout the infrastructure:

### Network Security

- **VPC isolation**: Separate public and private subnets
- **Security groups**: Least privilege access controls
- **Network ACLs**: Additional layer of network filtering
- **VPN access**: Secure administrative access

### Data Security

- **Encryption at rest**: All persistent data encrypted
- **Encryption in transit**: TLS for all communications
- **Key management**: Centralized key management service
- **Data classification**: Policies based on data sensitivity

### Access Control

- **IAM roles**: Fine-grained access control
- **RBAC**: Role-based access in Kubernetes
- **MFA**: Multi-factor authentication for administrative access
- **Least privilege**: Minimal permissions for each role

### Compliance

- **Audit logging**: Comprehensive audit trails
- **Compliance scanning**: Regular automated compliance checks
- **Vulnerability management**: Continuous vulnerability scanning
- **Penetration testing**: Regular security assessments

## Scaling Considerations

QuantumVest is designed to scale with increasing load:

### Horizontal Scaling

- **Stateless components**: Automatically scale based on CPU/memory usage
- **Database read replicas**: Scale read operations
- **Caching layer**: Reduce database load

### Vertical Scaling

- **Instance sizing**: Appropriate resource allocation
- **Database instance class**: Match to workload requirements
- **Performance optimization**: Regular performance tuning

### Geographic Scaling

- **Multi-region deployment**: Serve users from closest region
- **Content delivery network**: Cache static assets globally
- **Global database**: Distributed database for global presence

## Maintenance Procedures

Regular maintenance is essential for system health:

### Routine Maintenance

- **Security patches**: Regular patching schedule
- **Database maintenance**: Vacuum, reindex, analyze
- **Log rotation**: Prevent disk space issues
- **Backup verification**: Regular restore testing

### Deployment Process

- **Blue-green deployments**: Zero-downtime updates
- **Canary releases**: Gradual rollout of changes
- **Rollback procedure**: Quick recovery from failed deployments
- **Change management**: Documented approval process

### Incident Response

- **On-call rotation**: 24/7 coverage
- **Incident classification**: Severity levels and response times
- **Runbooks**: Step-by-step recovery procedures
- **Post-mortem process**: Learn from incidents

## Conclusion

This infrastructure guide provides a comprehensive overview of the QuantumVest platform's infrastructure. By following the practices outlined in this document, you can ensure a reliable, secure, and scalable deployment of the application.

For more detailed information, refer to the following resources:

- [Technical Documentation](./technical_documentation.md)
- [Developer Guide](./developer_guide.md)
- [API Documentation](./api_documentation.md)
