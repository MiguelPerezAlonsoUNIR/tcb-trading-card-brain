# Packer template for building GCP Image with TCB Trading Card Brain

packer {
  required_plugins {
    googlecompute = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/googlecompute"
    }
    ansible = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/ansible"
    }
  }
}

variable "gcp_project_id" {
  type    = string
  default = "${env("GCP_PROJECT_ID")}"
}

variable "gcp_zone" {
  type    = string
  default = "us-east1-b"
}

variable "image_name_prefix" {
  type    = string
  default = "tcb-trading-card-brain"
}

variable "machine_type" {
  type    = string
  default = "e2-medium"
}

variable "ssh_username" {
  type    = string
  default = "packer"
}

locals {
  timestamp = regex_replace(timestamp(), "[- TZ:]", "")
}

source "googlecompute" "ubuntu" {
  project_id   = var.gcp_project_id
  source_image_family = "ubuntu-2204-lts"
  zone         = var.gcp_zone
  machine_type = var.machine_type
  
  image_name        = "${var.image_name_prefix}-${local.timestamp}"
  image_description = "TCB Trading Card Brain application image"
  image_family      = var.image_name_prefix
  
  ssh_username = var.ssh_username
  
  labels = {
    name        = "${var.image_name_prefix}-${local.timestamp}"
    environment = "production"
    builder     = "packer"
    os          = "ubuntu-2204"
  }
}

build {
  name = "tcb-app-gcp-image"
  sources = [
    "source.googlecompute.ubuntu"
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
