#!/bin/bash
# User data script for Azure VM initialization

# Update system packages
apt-get update
apt-get upgrade -y

# Install required packages
apt-get install -y \
    python3.11 \
    python3-pip \
    python3-venv \
    git \
    nginx \
    supervisor \
    docker.io \
    docker-compose

# Enable and start services
systemctl enable docker
systemctl start docker

# Create application user
useradd -m -s /bin/bash tcbapp

# Create application directory
mkdir -p /opt/tcb-trading-card-brain
chown tcbapp:tcbapp /opt/tcb-trading-card-brain

# Log the completion
echo "User data script completed at $(date)" >> /var/log/user-data.log
