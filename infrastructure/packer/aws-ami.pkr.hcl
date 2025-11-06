# Packer template for building AWS AMI with TCB Trading Card Brain

packer {
  required_plugins {
    amazon = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/amazon"
    }
    ansible = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/ansible"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "instance_type" {
  type    = string
  default = "t3.small"
}

variable "ami_name_prefix" {
  type    = string
  default = "tcb-trading-card-brain"
}

variable "ssh_username" {
  type    = string
  default = "ubuntu"
}

locals {
  timestamp = regex_replace(timestamp(), "[- TZ:]", "")
}

source "amazon-ebs" "ubuntu" {
  ami_name      = "${var.ami_name_prefix}-${local.timestamp}"
  instance_type = var.instance_type
  region        = var.aws_region
  
  source_ami_filter {
    filters = {
      name                = "ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }
    most_recent = true
    owners      = ["099720109477"] # Canonical
  }
  
  ssh_username = var.ssh_username
  
  tags = {
    Name        = "${var.ami_name_prefix}-${local.timestamp}"
    Environment = "production"
    Builder     = "Packer"
    OS          = "Ubuntu 22.04"
  }
}

build {
  name = "tcb-app-ami"
  sources = [
    "source.amazon-ebs.ubuntu"
  ]
  
  # Update system packages
  provisioner "shell" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get upgrade -y",
      "sudo apt-get install -y python3-pip python3-venv"
    ]
  }
  
  # Run Ansible playbook
  provisioner "ansible" {
    playbook_file = "../ansible/playbooks/deploy-app.yml"
    extra_arguments = [
      "--extra-vars",
      "ansible_python_interpreter=/usr/bin/python3"
    ]
  }
  
  # Clean up
  provisioner "shell" {
    inline = [
      "sudo apt-get clean",
      "sudo rm -rf /tmp/*",
      "sudo rm -rf /var/tmp/*",
      "history -c"
    ]
  }
}
