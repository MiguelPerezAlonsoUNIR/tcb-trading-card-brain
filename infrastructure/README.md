# TCB Trading Card Brain - Infrastructure Deployment

This directory contains Infrastructure as Code (IaC) configurations for deploying the TCB Trading Card Brain application to multiple cloud providers (AWS, Azure, GCP) and local development environments.

## Directory Structure

```
infrastructure/
├── terraform/           # Infrastructure provisioning
│   ├── aws/            # AWS-specific Terraform configuration
│   ├── azure/          # Azure-specific Terraform configuration
│   ├── gcp/            # GCP-specific Terraform configuration
│   └── modules/        # Reusable Terraform modules
├── ansible/            # Configuration management
│   ├── playbooks/      # Ansible playbooks
│   ├── roles/          # Ansible roles
│   │   ├── common/     # Common system setup
│   │   ├── app/        # Application deployment
│   │   ├── nginx/      # Web server configuration
│   │   └── database/   # Database setup
│   └── inventory/      # Inventory files
├── packer/             # Machine image building
│   ├── aws-ami.pkr.hcl       # AWS AMI template
│   ├── azure-image.pkr.hcl   # Azure Image template
│   └── gcp-image.pkr.hcl     # GCP Image template
└── vagrant/            # Local development environment
    └── Vagrantfile     # Vagrant configuration
```

## Prerequisites

### Required Tools

1. **Terraform** (>= 1.0)
   ```bash
   # Install on Linux
   wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
   unzip terraform_1.6.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/
   ```

2. **Ansible** (>= 2.9)
   ```bash
   # Install on Ubuntu/Debian
   sudo apt update
   sudo apt install ansible
   
   # Install on macOS
   brew install ansible
   ```

3. **Packer** (>= 1.8)
   ```bash
   # Install on Linux
   wget https://releases.hashicorp.com/packer/1.9.0/packer_1.9.0_linux_amd64.zip
   unzip packer_1.9.0_linux_amd64.zip
   sudo mv packer /usr/local/bin/
   ```

4. **Vagrant** (>= 2.3) - For local testing
   ```bash
   # Install on Ubuntu/Debian
   wget https://releases.hashicorp.com/vagrant/2.4.0/vagrant_2.4.0_linux_amd64.zip
   
   # Install on macOS
   brew install vagrant
   ```

5. **Cloud CLI Tools**
   - AWS CLI (`aws`)
   - Azure CLI (`az`)
   - Google Cloud SDK (`gcloud`)

## Deployment Strategies

### Strategy 1: Direct Deployment with Terraform + Ansible

**Best for:** Quick deployments, development environments

1. Provision infrastructure with Terraform
2. Configure and deploy application with Ansible

### Strategy 2: Pre-built Images with Packer + Terraform

**Best for:** Production environments, faster scaling, immutable infrastructure

1. Build custom machine images with Packer
2. Deploy instances using pre-built images with Terraform

### Strategy 3: Local Testing with Vagrant

**Best for:** Local development, testing infrastructure changes

1. Test deployment locally with Vagrant
2. Validate Ansible playbooks before production deployment

## Quick Start Guides

### AWS Deployment

#### 1. Configure AWS Credentials

```bash
# Configure AWS CLI
aws configure

# Or export credentials
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

#### 2. Create SSH Key Pair

```bash
# Create key pair in AWS
aws ec2 create-key-pair --key-name tcb-app-key --query 'KeyMaterial' --output text > ~/.ssh/tcb-app-key.pem
chmod 400 ~/.ssh/tcb-app-key.pem
```

#### 3. Deploy with Terraform

```bash
cd terraform/aws

# Create terraform.tfvars
cat > terraform.tfvars <<EOF
key_name = "tcb-app-key"
environment = "production"
db_password = "your-secure-password"
EOF

# Initialize and apply
terraform init
terraform plan
terraform apply
```

#### 4. Configure with Ansible

```bash
cd ../../ansible

# Get the public IP from Terraform output
export APP_IP=$(cd ../terraform/aws && terraform output -raw public_ip)

# Update inventory
cat > inventory/hosts <<EOF
[app_servers]
aws-app ansible_host=$APP_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/tcb-app-key.pem
EOF

# Deploy application
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml
```

### Azure Deployment

#### 1. Configure Azure Credentials

```bash
# Login to Azure
az login

# Set subscription
az account set --subscription "your-subscription-id"

# Create service principal for Terraform
az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/your-subscription-id"
```

#### 2. Create SSH Key

```bash
# Generate SSH key if you don't have one
ssh-keygen -t rsa -b 4096 -f ~/.ssh/tcb-azure-key
```

#### 3. Deploy with Terraform

```bash
cd terraform/azure

# Create terraform.tfvars
cat > terraform.tfvars <<EOF
ssh_public_key = "$(cat ~/.ssh/tcb-azure-key.pub)"
environment = "production"
db_password = "your-secure-password"
EOF

# Initialize and apply
terraform init
terraform plan
terraform apply
```

#### 4. Configure with Ansible

```bash
cd ../../ansible

# Get the public IP from Terraform output
export APP_IP=$(cd ../terraform/azure && terraform output -raw public_ip)

# Update inventory
cat > inventory/hosts <<EOF
[app_servers]
azure-app ansible_host=$APP_IP ansible_user=azureuser ansible_ssh_private_key_file=~/.ssh/tcb-azure-key
EOF

# Deploy application
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml
```

### GCP Deployment

#### 1. Configure GCP Credentials

```bash
# Login to GCP
gcloud auth login

# Set project
gcloud config set project your-project-id

# Create service account for Terraform
gcloud iam service-accounts create terraform-sa
gcloud projects add-iam-policy-binding your-project-id \
  --member="serviceAccount:terraform-sa@your-project-id.iam.gserviceaccount.com" \
  --role="roles/editor"

# Download service account key
gcloud iam service-accounts keys create ~/gcp-terraform-key.json \
  --iam-account=terraform-sa@your-project-id.iam.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS=~/gcp-terraform-key.json
```

#### 2. Create SSH Key

```bash
# Generate SSH key if you don't have one
ssh-keygen -t rsa -b 4096 -f ~/.ssh/tcb-gcp-key
```

#### 3. Deploy with Terraform

```bash
cd terraform/gcp

# Create terraform.tfvars
cat > terraform.tfvars <<EOF
project_id = "your-project-id"
ssh_public_key = "$(cat ~/.ssh/tcb-gcp-key.pub)"
environment = "production"
db_password = "your-secure-password"
EOF

# Initialize and apply
terraform init
terraform plan
terraform apply
```

#### 4. Configure with Ansible

```bash
cd ../../ansible

# Get the public IP from Terraform output
export APP_IP=$(cd ../terraform/gcp && terraform output -raw public_ip)

# Update inventory
cat > inventory/hosts <<EOF
[app_servers]
gcp-app ansible_host=$APP_IP ansible_user=gcpuser ansible_ssh_private_key_file=~/.ssh/tcb-gcp-key
EOF

# Deploy application
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml
```

## Building Custom Images with Packer

### Why Use Packer?

Packer creates pre-configured machine images that:
- **Reduce deployment time**: Images are pre-provisioned with all dependencies
- **Ensure consistency**: Same image across all instances
- **Enable immutable infrastructure**: Deploy new instances instead of updating existing ones
- **Simplify scaling**: New instances are ready immediately

### Build AWS AMI

```bash
cd packer

# Build AMI
packer init aws-ami.pkr.hcl
packer build aws-ami.pkr.hcl

# Use the AMI ID in Terraform
cd ../terraform/aws
terraform apply -var="ami_id=ami-xxxxxxxxxxxxx"
```

### Build Azure Image

```bash
cd packer

# Set Azure credentials
export AZURE_CLIENT_ID="your-client-id"
export AZURE_CLIENT_SECRET="your-client-secret"
export AZURE_SUBSCRIPTION_ID="your-subscription-id"
export AZURE_TENANT_ID="your-tenant-id"

# Create resource group for images
az group create --name tcb-images-rg --location eastus

# Build image
packer init azure-image.pkr.hcl
packer build azure-image.pkr.hcl
```

### Build GCP Image

```bash
cd packer

# Set GCP project
export GCP_PROJECT_ID="your-project-id"

# Build image
packer init gcp-image.pkr.hcl
packer build gcp-image.pkr.hcl

# Use the image in Terraform
cd ../terraform/gcp
terraform apply -var="image_id=tcb-trading-card-brain-xxxxxxxxxxxxx"
```

## Local Testing with Vagrant

### Why Use Vagrant?

Vagrant provides:
- **Local testing**: Test infrastructure changes without cloud costs
- **Development environment**: Consistent dev environment for all team members
- **Validation**: Validate Ansible playbooks before production deployment
- **Debugging**: Easy access to logs and troubleshooting

### Start Local Environment

```bash
cd vagrant

# Start VM and provision
vagrant up

# Access the application
# Flask: http://localhost:5000
# Nginx: http://localhost:8080

# SSH into VM
vagrant ssh

# View logs
vagrant ssh -c "sudo journalctl -u tcb-app -f"

# Destroy VM when done
vagrant destroy
```

### Vagrant Commands

```bash
vagrant up        # Start and provision VM
vagrant halt      # Stop VM
vagrant reload    # Restart VM
vagrant provision # Re-run provisioning
vagrant destroy   # Delete VM
vagrant ssh       # SSH into VM
vagrant status    # Check VM status
```

## Configuration Management with Ansible

### Ansible Roles

#### Common Role
Sets up base system requirements:
- System updates
- Essential packages
- Python 3.11
- Docker
- Firewall configuration

#### App Role
Deploys the application:
- Clones repository
- Creates virtual environment
- Installs dependencies
- Configures systemd service
- Initializes database

#### Nginx Role
Configures web server:
- Installs Nginx
- Sets up reverse proxy
- Configures SSL (optional)

#### Database Role
Sets up PostgreSQL:
- Installs PostgreSQL
- Creates database and user
- Configures authentication

### Custom Variables

Create a `group_vars/all.yml` file:

```yaml
# Application settings
app_name: tcb-trading-card-brain
app_user: tcbapp
app_dir: /opt/tcb-trading-card-brain
repo_url: https://github.com/MiguelPerezAlonsoUNIR/tcb-trading-card-brain.git
repo_branch: main

# Flask settings
secret_key: "{{ vault_secret_key }}"
flask_env: production
gunicorn_workers: 4

# Database settings (if using PostgreSQL)
database_url: "postgresql://{{ db_user }}:{{ db_password }}@localhost/{{ db_name }}"
db_name: tcb_db
db_user: tcbapp
db_password: "{{ vault_db_password }}"

# Nginx settings
server_name: your-domain.com
```

### Using Ansible Vault for Secrets

```bash
# Create vault file
ansible-vault create group_vars/vault.yml

# Add secrets
vault_secret_key: your-secret-key
vault_db_password: your-db-password

# Run playbook with vault
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml --ask-vault-pass
```

## Maintenance and Operations

### Update Application

```bash
# Using Ansible
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml --tags update

# Manual update
ssh ubuntu@your-server-ip
cd /opt/tcb-trading-card-brain
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart tcb-app
```

### View Logs

```bash
# Application logs
sudo journalctl -u tcb-app -f

# Nginx logs
sudo tail -f /var/log/nginx/tcb-app-access.log
sudo tail -f /var/log/nginx/tcb-app-error.log

# System logs
sudo journalctl -xe
```

### Backup Database

```bash
# SQLite backup
scp ubuntu@your-server-ip:/opt/tcb-trading-card-brain/tcb.db ./backup-$(date +%Y%m%d).db

# PostgreSQL backup
ssh ubuntu@your-server-ip "sudo -u postgres pg_dump tcb_db" > backup-$(date +%Y%m%d).sql
```

### Scale Infrastructure

#### AWS Auto Scaling

```bash
cd terraform/aws
# Modify main.tf to add Auto Scaling Group
terraform plan
terraform apply
```

#### Azure Scale Sets

```bash
cd terraform/azure
# Modify main.tf to add Virtual Machine Scale Set
terraform plan
terraform apply
```

## Security Best Practices

1. **Use Secrets Management**
   - AWS: AWS Secrets Manager or Parameter Store
   - Azure: Azure Key Vault
   - GCP: Secret Manager
   - Ansible: Ansible Vault

2. **Enable HTTPS**
   - Use Let's Encrypt for free SSL certificates
   - Configure Nginx with SSL/TLS

3. **Restrict SSH Access**
   - Update `ssh_allowed_ips` variable in Terraform
   - Use VPN or bastion host for production

4. **Regular Updates**
   - Keep system packages updated
   - Update Python dependencies regularly
   - Monitor security advisories

5. **Network Security**
   - Use private subnets for databases
   - Enable firewall rules
   - Configure security groups properly

## Troubleshooting

### Terraform Issues

```bash
# View detailed logs
export TF_LOG=DEBUG
terraform apply

# Fix state lock issues
terraform force-unlock LOCK_ID

# Refresh state
terraform refresh
```

### Ansible Issues

```bash
# Run in verbose mode
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml -vvv

# Test connectivity
ansible -i inventory/hosts all -m ping

# Check syntax
ansible-playbook --syntax-check playbooks/deploy-app.yml
```

### Packer Issues

```bash
# Enable debug mode
packer build -debug aws-ami.pkr.hcl

# Validate template
packer validate aws-ami.pkr.hcl
```

### Application Issues

```bash
# Check service status
sudo systemctl status tcb-app

# Restart service
sudo systemctl restart tcb-app

# Check Python dependencies
cd /opt/tcb-trading-card-brain
source venv/bin/activate
pip list
```

## Cost Optimization

### AWS
- Use Reserved Instances for long-term deployments
- Enable Auto Scaling for variable load
- Use t3.micro or t3.small for development

### Azure
- Use B-series VMs for cost-effective deployments
- Enable auto-shutdown for dev environments
- Use Azure Hybrid Benefit if applicable

### GCP
- Use e2-micro or e2-small for development
- Enable sustained use discounts
- Use preemptible VMs for non-critical workloads

## Support and Contributing

For issues or questions:
1. Check the troubleshooting section
2. Review Terraform/Ansible/Packer documentation
3. Open an issue on GitHub

## License

This infrastructure code is part of the TCB Trading Card Brain project and follows the same license.
