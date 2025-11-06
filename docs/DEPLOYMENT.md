# TCB Trading Card Brain - Deployment Guide

This guide provides detailed instructions for deploying the TCB Trading Card Brain application to various cloud providers and local environments.

## Table of Contents

1. [Overview](#overview)
2. [Infrastructure Options](#infrastructure-options)
3. [Prerequisites](#prerequisites)
4. [Deployment Methods](#deployment-methods)
5. [Cloud Provider Guides](#cloud-provider-guides)
6. [Local Development](#local-development)
7. [Post-Deployment](#post-deployment)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)

## Overview

The TCB Trading Card Brain application can be deployed using multiple approaches:

- **Direct Deployment**: Quick deployment using Terraform + Ansible
- **Image-based Deployment**: Production-ready deployment using Packer + Terraform
- **Local Development**: Test locally using Vagrant

## Infrastructure Options

### Supported Cloud Providers

- **AWS (Amazon Web Services)**: Deploy to EC2 with optional RDS PostgreSQL
- **Azure (Microsoft Azure)**: Deploy to Virtual Machines with optional Azure Database
- **GCP (Google Cloud Platform)**: Deploy to Compute Engine with optional Cloud SQL

### Architecture

Each deployment includes:
- **Compute**: VM instance running the Flask application
- **Networking**: VPC/VNet with public and private subnets
- **Load Balancing**: Nginx reverse proxy
- **Database**: SQLite (default) or PostgreSQL (optional)
- **Security**: Firewall rules and security groups

## Prerequisites

### Required Tools

Install the following tools on your local machine:

1. **Terraform** (>= 1.0)
   ```bash
   wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
   unzip terraform_1.6.0_linux_amd64.zip
   sudo mv terraform /usr/local/bin/
   terraform --version
   ```

2. **Ansible** (>= 2.9)
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install ansible
   
   # macOS
   brew install ansible
   
   ansible --version
   ```

3. **Cloud CLI** (choose based on your provider)
   ```bash
   # AWS CLI
   curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
   unzip awscliv2.zip
   sudo ./aws/install
   
   # Azure CLI
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   
   # Google Cloud SDK
   curl https://sdk.cloud.google.com | bash
   ```

### Cloud Provider Accounts

- AWS: Create an AWS account and obtain access keys
- Azure: Create an Azure account and subscription
- GCP: Create a GCP project and enable billing

## Deployment Methods

### Method 1: Direct Deployment (Recommended for Development)

**Steps:**
1. Provision infrastructure with Terraform
2. Configure servers with Ansible
3. Deploy application code

**Advantages:**
- Quick setup
- Easy to modify
- Good for development

**Time:** ~10-15 minutes

### Method 2: Image-based Deployment (Recommended for Production)

**Steps:**
1. Build custom images with Packer
2. Deploy instances using pre-built images with Terraform

**Advantages:**
- Faster scaling
- Immutable infrastructure
- Consistent deployments

**Time:** ~30 minutes (first build), ~5 minutes (subsequent deployments)

### Method 3: Container Deployment

**Steps:**
1. Use existing Docker configuration
2. Deploy to cloud container services

**Advantages:**
- Lightweight
- Portable
- Easy scaling

**Time:** ~5-10 minutes

## Cloud Provider Guides

### AWS Deployment

#### Step 1: Configure AWS Credentials

```bash
# Option 1: Using AWS CLI
aws configure
# Enter your Access Key ID, Secret Access Key, and default region

# Option 2: Using environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="us-east-1"
```

#### Step 2: Create SSH Key Pair

```bash
# Create key pair in AWS
aws ec2 create-key-pair --key-name tcb-app-key --query 'KeyMaterial' --output text > ~/.ssh/tcb-app-key.pem
chmod 400 ~/.ssh/tcb-app-key.pem
```

#### Step 3: Configure Terraform Variables

```bash
cd infrastructure/terraform/aws
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your settings
```

#### Step 4: Deploy Infrastructure

```bash
# Initialize Terraform
terraform init

# Review planned changes
terraform plan

# Apply changes
terraform apply
```

#### Step 5: Deploy Application

```bash
cd ../../ansible

# Get the public IP from Terraform
export APP_IP=$(cd ../terraform/aws && terraform output -raw public_ip)

# Create inventory file
cat > inventory/hosts <<EOF
[app_servers]
aws-app ansible_host=$APP_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/tcb-app-key.pem
EOF

# Deploy application
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml
```

#### Quick Deployment Script

```bash
# Use the automated script
cd infrastructure/scripts
./deploy-aws.sh
```

### Azure Deployment

#### Step 1: Configure Azure Credentials

```bash
# Login to Azure
az login

# List subscriptions
az account list --output table

# Set active subscription
az account set --subscription "Your-Subscription-ID"
```

#### Step 2: Create Service Principal (for Terraform)

```bash
az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/YOUR-SUBSCRIPTION-ID"
# Note the output values for Terraform
```

#### Step 3: Generate SSH Key

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/tcb-azure-key
```

#### Step 4: Deploy Infrastructure

```bash
cd infrastructure/terraform/azure
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your settings

terraform init
terraform plan
terraform apply
```

#### Step 5: Deploy Application

```bash
cd ../../ansible
export APP_IP=$(cd ../terraform/azure && terraform output -raw public_ip)

cat > inventory/hosts <<EOF
[app_servers]
azure-app ansible_host=$APP_IP ansible_user=azureuser ansible_ssh_private_key_file=~/.ssh/tcb-azure-key
EOF

ansible-playbook -i inventory/hosts playbooks/deploy-app.yml
```

### GCP Deployment

#### Step 1: Configure GCP Credentials

```bash
# Login to GCP
gcloud auth login

# Set project
gcloud config set project YOUR-PROJECT-ID

# Create service account for Terraform
gcloud iam service-accounts create terraform-sa

# Grant permissions
gcloud projects add-iam-policy-binding YOUR-PROJECT-ID \
  --member="serviceAccount:terraform-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com" \
  --role="roles/editor"

# Create and download key
gcloud iam service-accounts keys create ~/gcp-terraform-key.json \
  --iam-account=terraform-sa@YOUR-PROJECT-ID.iam.gserviceaccount.com

# Set credentials
export GOOGLE_APPLICATION_CREDENTIALS=~/gcp-terraform-key.json
```

#### Step 2: Generate SSH Key

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/tcb-gcp-key
```

#### Step 3: Deploy Infrastructure

```bash
cd infrastructure/terraform/gcp
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your settings

terraform init
terraform plan
terraform apply
```

#### Step 4: Deploy Application

```bash
cd ../../ansible
export APP_IP=$(cd ../terraform/gcp && terraform output -raw public_ip)

cat > inventory/hosts <<EOF
[app_servers]
gcp-app ansible_host=$APP_IP ansible_user=gcpuser ansible_ssh_private_key_file=~/.ssh/tcb-gcp-key
EOF

ansible-playbook -i inventory/hosts playbooks/deploy-app.yml
```

## Local Development

### Using Vagrant

Vagrant provides a local VM for testing the infrastructure:

#### Step 1: Install Prerequisites

```bash
# Install VirtualBox
sudo apt install virtualbox

# Install Vagrant
wget https://releases.hashicorp.com/vagrant/2.4.0/vagrant_2.4.0_linux_amd64.zip
unzip vagrant_2.4.0_linux_amd64.zip
sudo mv vagrant /usr/local/bin/
```

#### Step 2: Start Local Environment

```bash
cd infrastructure/vagrant
vagrant up
```

#### Step 3: Access Application

- Flask (direct): http://localhost:5000
- Nginx (proxy): http://localhost:8080

#### Step 4: Manage VM

```bash
# SSH into VM
vagrant ssh

# View logs
vagrant ssh -c "sudo journalctl -u tcb-app -f"

# Stop VM
vagrant halt

# Restart VM
vagrant reload

# Destroy VM
vagrant destroy
```

## Post-Deployment

### Verify Deployment

```bash
# Check if application is running
curl http://YOUR-SERVER-IP:5000

# Check via Nginx
curl http://YOUR-SERVER-IP
```

### Access the Application

Open your browser and navigate to:
```
http://YOUR-SERVER-IP
```

### Initial Setup

1. Register a new user account
2. Add cards to your collection
3. Build your first deck

## Monitoring and Maintenance

### View Application Logs

```bash
# Application logs
sudo journalctl -u tcb-app -f

# Nginx access logs
sudo tail -f /var/log/nginx/tcb-app-access.log

# Nginx error logs
sudo tail -f /var/log/nginx/tcb-app-error.log
```

### Update Application

```bash
# Using Ansible
cd infrastructure/ansible
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml

# Manual update
ssh ubuntu@YOUR-SERVER-IP
cd /opt/tcb-trading-card-brain
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart tcb-app
```

### Backup Database

```bash
# SQLite database
scp ubuntu@YOUR-SERVER-IP:/opt/tcb-trading-card-brain/tcb.db ./backup-$(date +%Y%m%d).db

# PostgreSQL database
ssh ubuntu@YOUR-SERVER-IP "sudo -u postgres pg_dump tcb_db" > backup-$(date +%Y%m%d).sql
```

### Scale Resources

#### Vertical Scaling (Increase VM Size)

```bash
cd infrastructure/terraform/aws
# Edit terraform.tfvars: instance_type = "t3.medium"
terraform apply
```

#### Horizontal Scaling (Add More Instances)

- Modify Terraform configuration to add auto-scaling
- Use load balancer for distributing traffic

## Security Best Practices

1. **Change Default Passwords**: Update all default passwords in terraform.tfvars
2. **Restrict SSH Access**: Limit SSH to specific IP addresses
3. **Enable HTTPS**: Configure SSL certificates for production
4. **Use Secrets Management**: Store sensitive data in cloud secret managers
5. **Regular Updates**: Keep system packages and dependencies updated

## Troubleshooting

### Common Issues

#### Terraform Issues

**Problem**: Terraform state lock
```bash
# Force unlock (use with caution)
terraform force-unlock LOCK_ID
```

**Problem**: Authentication errors
```bash
# Verify credentials
aws sts get-caller-identity  # AWS
az account show              # Azure
gcloud auth list             # GCP
```

#### Ansible Issues

**Problem**: Connection timeout
```bash
# Test connectivity
ansible -i inventory/hosts all -m ping

# Increase timeout
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml --timeout=300
```

**Problem**: Permission denied
```bash
# Check SSH key permissions
chmod 400 ~/.ssh/your-key.pem

# Verify SSH access
ssh -i ~/.ssh/your-key.pem ubuntu@YOUR-SERVER-IP
```

#### Application Issues

**Problem**: Application not starting
```bash
# Check service status
sudo systemctl status tcb-app

# View detailed logs
sudo journalctl -u tcb-app -n 50 --no-pager

# Restart service
sudo systemctl restart tcb-app
```

**Problem**: Database errors
```bash
# Reinitialize database
cd /opt/tcb-trading-card-brain
source venv/bin/activate
python init_cards_db.py
```

## Cost Estimates

### AWS
- **Development**: ~$10-20/month (t3.micro)
- **Production**: ~$50-100/month (t3.small + RDS)

### Azure
- **Development**: ~$15-25/month (B1s)
- **Production**: ~$60-120/month (B2s + Database)

### GCP
- **Development**: ~$12-22/month (e2-micro)
- **Production**: ~$55-110/month (e2-small + Cloud SQL)

*Note: Costs vary based on region, usage, and additional services.*

## Next Steps

1. **Configure Domain**: Point your domain to the server IP
2. **Setup SSL**: Use Let's Encrypt for free SSL certificates
3. **Enable Monitoring**: Set up CloudWatch/Azure Monitor/Stackdriver
4. **Backup Strategy**: Implement automated backups
5. **CI/CD Pipeline**: Automate deployments with GitHub Actions

## Support

For issues or questions:
- Check the [Infrastructure README](../infrastructure/README.md)
- Review cloud provider documentation
- Open an issue on GitHub

## References

- [Terraform Documentation](https://www.terraform.io/docs)
- [Ansible Documentation](https://docs.ansible.com/)
- [Packer Documentation](https://www.packer.io/docs)
- [Vagrant Documentation](https://www.vagrantup.com/docs)
