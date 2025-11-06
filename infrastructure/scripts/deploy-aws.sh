#!/bin/bash
# Quick deployment script for AWS

set -e

echo "=========================================="
echo "TCB Trading Card Brain - AWS Deployment"
echo "=========================================="

# Check prerequisites
command -v terraform >/dev/null 2>&1 || { echo "Error: terraform is required but not installed." >&2; exit 1; }
command -v ansible >/dev/null 2>&1 || { echo "Error: ansible is required but not installed." >&2; exit 1; }
command -v aws >/dev/null 2>&1 || { echo "Error: aws cli is required but not installed." >&2; exit 1; }

# Navigate to AWS terraform directory
cd "$(dirname "$0")/../terraform/aws"

# Check if terraform.tfvars exists
if [ ! -f terraform.tfvars ]; then
    echo "Error: terraform.tfvars not found!"
    echo "Please copy terraform.tfvars.example to terraform.tfvars and configure it."
    exit 1
fi

# Initialize Terraform
echo ""
echo "Initializing Terraform..."
terraform init

# Plan
echo ""
echo "Planning infrastructure changes..."
terraform plan -out=tfplan

# Ask for confirmation
echo ""
read -p "Do you want to apply these changes? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Deployment cancelled."
    exit 0
fi

# Apply
echo ""
echo "Applying infrastructure changes..."
terraform apply tfplan

# Get outputs
echo ""
echo "Getting infrastructure details..."
PUBLIC_IP=$(terraform output -raw public_ip)
echo "Instance Public IP: $PUBLIC_IP"

# Update Ansible inventory
echo ""
echo "Updating Ansible inventory..."
cd ../../ansible
cat > inventory/hosts <<EOF
[app_servers]
aws-app ansible_host=$PUBLIC_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/$(cd ../terraform/aws && terraform output -raw key_name).pem

[app_servers:vars]
app_name=tcb-trading-card-brain
app_user=tcbapp
app_dir=/opt/tcb-trading-card-brain
repo_url=https://github.com/MiguelPerezAlonsoUNIR/tcb-trading-card-brain.git
repo_branch=main
secret_key=${SECRET_KEY:-$(openssl rand -hex 32)}
database_url=sqlite:///tcb.db
flask_env=production
gunicorn_workers=2
initialize_db=true
EOF

# Wait for instance to be ready
echo ""
echo "Waiting for instance to be ready (60 seconds)..."
sleep 60

# Deploy application with Ansible
echo ""
echo "Deploying application with Ansible..."
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml

echo ""
echo "=========================================="
echo "Deployment complete!"
echo "Application URL: http://$PUBLIC_IP"
echo "=========================================="
