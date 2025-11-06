# Infrastructure Quick Start Guide

This is a quick reference guide for deploying the TCB Trading Card Brain application. For detailed documentation, see [README.md](README.md) and [DEPLOYMENT.md](../docs/DEPLOYMENT.md).

## Prerequisites

Install these tools before starting:

```bash
# Terraform
wget https://releases.hashicorp.com/terraform/1.6.0/terraform_1.6.0_linux_amd64.zip
unzip terraform_1.6.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Ansible
sudo apt install ansible

# AWS CLI (for AWS deployment)
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
```

## Option 1: Local Testing with Vagrant (5 minutes)

```bash
# Install Vagrant
sudo apt install virtualbox vagrant

# Start local environment
cd infrastructure/vagrant
vagrant up

# Access application
# - Flask: http://localhost:5000
# - Nginx: http://localhost:8080

# When done
vagrant destroy
```

## Option 2: AWS Deployment (15 minutes)

```bash
# 1. Configure AWS credentials
aws configure

# 2. Create SSH key
aws ec2 create-key-pair --key-name tcb-app-key --query 'KeyMaterial' --output text > ~/.ssh/tcb-app-key.pem
chmod 400 ~/.ssh/tcb-app-key.pem

# 3. Configure Terraform
cd infrastructure/terraform/aws
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your settings

# 4. Deploy infrastructure
terraform init
terraform apply

# 5. Deploy application
cd ../../ansible
export APP_IP=$(cd ../terraform/aws && terraform output -raw public_ip)
cat > inventory/hosts <<EOF
[app_servers]
aws-app ansible_host=$APP_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/tcb-app-key.pem
EOF

# Wait for instance to be ready
sleep 60

ansible-playbook -i inventory/hosts playbooks/deploy-app.yml

# Access at: http://$APP_IP
```

## Option 3: Azure Deployment (15 minutes)

```bash
# 1. Login to Azure
az login

# 2. Generate SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/tcb-azure-key

# 3. Configure Terraform
cd infrastructure/terraform/azure
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your settings

# 4. Deploy infrastructure
terraform init
terraform apply

# 5. Deploy application
cd ../../ansible
export APP_IP=$(cd ../terraform/azure && terraform output -raw public_ip)
cat > inventory/hosts <<EOF
[app_servers]
azure-app ansible_host=$APP_IP ansible_user=azureuser ansible_ssh_private_key_file=~/.ssh/tcb-azure-key
EOF

sleep 60
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml

# Access at: http://$APP_IP
```

## Option 4: GCP Deployment (15 minutes)

```bash
# 1. Login to GCP
gcloud auth login
gcloud config set project YOUR-PROJECT-ID

# 2. Generate SSH key
ssh-keygen -t rsa -b 4096 -f ~/.ssh/tcb-gcp-key

# 3. Configure Terraform
cd infrastructure/terraform/gcp
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with your settings

# 4. Deploy infrastructure
terraform init
terraform apply

# 5. Deploy application
cd ../../ansible
export APP_IP=$(cd ../terraform/gcp && terraform output -raw public_ip)
cat > inventory/hosts <<EOF
[app_servers]
gcp-app ansible_host=$APP_IP ansible_user=gcpuser ansible_ssh_private_key_file=~/.ssh/tcb-gcp-key
EOF

sleep 60
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml

# Access at: http://$APP_IP
```

## Common Commands

### View Application Logs
```bash
ssh ubuntu@YOUR-SERVER-IP "sudo journalctl -u tcb-app -f"
```

### Update Application
```bash
cd infrastructure/ansible
ansible-playbook -i inventory/hosts playbooks/deploy-app.yml
```

### Destroy Infrastructure
```bash
cd infrastructure/terraform/[aws|azure|gcp]
terraform destroy
```

### Check Application Status
```bash
ssh ubuntu@YOUR-SERVER-IP "sudo systemctl status tcb-app"
```

## Troubleshooting

### Can't connect to server
```bash
# Check if instance is running
aws ec2 describe-instances --filters "Name=tag:Name,Values=tcb-*"

# Verify SSH key permissions
chmod 400 ~/.ssh/your-key.pem

# Test SSH connection
ssh -i ~/.ssh/your-key.pem ubuntu@YOUR-SERVER-IP
```

### Application not starting
```bash
# SSH into server
ssh -i ~/.ssh/your-key.pem ubuntu@YOUR-SERVER-IP

# Check service status
sudo systemctl status tcb-app

# View logs
sudo journalctl -u tcb-app -n 50
```

### Terraform errors
```bash
# Verify credentials
aws sts get-caller-identity  # AWS
az account show              # Azure
gcloud auth list             # GCP

# Reinitialize Terraform
terraform init -upgrade
```

## Next Steps

1. **Configure Domain**: Point your domain to the server IP
2. **Setup SSL**: Use Let's Encrypt for HTTPS
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```
3. **Enable Monitoring**: Set up CloudWatch/Azure Monitor/Stackdriver
4. **Create Backups**: Set up automated database backups

## Additional Resources

- [Full README](README.md) - Complete infrastructure documentation
- [Deployment Guide](../docs/DEPLOYMENT.md) - Detailed deployment instructions
- [Infrastructure Analysis](ANALYSIS.md) - Tool comparison and recommendations
- [Terraform Docs](https://www.terraform.io/docs)
- [Ansible Docs](https://docs.ansible.com/)

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the full documentation
3. Open an issue on GitHub

## Security Reminder

⚠️ **Important**: Before production deployment:
1. Change all default passwords in `terraform.tfvars`
2. Restrict SSH access to specific IPs
3. Enable HTTPS with valid SSL certificates
4. Use secrets management for sensitive data
5. Enable firewall rules
