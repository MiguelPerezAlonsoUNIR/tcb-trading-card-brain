# Packer template for building Azure Image with TCB Trading Card Brain

packer {
  required_plugins {
    azure = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/azure"
    }
    ansible = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/ansible"
    }
  }
}

variable "azure_resource_group" {
  type    = string
  default = "tcb-images-rg"
}

variable "azure_location" {
  type    = string
  default = "eastus"
}

variable "image_name_prefix" {
  type    = string
  default = "tcb-trading-card-brain"
}

variable "vm_size" {
  type    = string
  default = "Standard_B2s"
}

variable "ssh_username" {
  type    = string
  default = "azureuser"
}

locals {
  timestamp = regex_replace(timestamp(), "[- TZ:]", "")
}

source "azure-arm" "ubuntu" {
  client_id       = "${env("AZURE_CLIENT_ID")}"
  client_secret   = "${env("AZURE_CLIENT_SECRET")}"
  subscription_id = "${env("AZURE_SUBSCRIPTION_ID")}"
  tenant_id       = "${env("AZURE_TENANT_ID")}"
  
  managed_image_resource_group_name = var.azure_resource_group
  managed_image_name                = "${var.image_name_prefix}-${local.timestamp}"
  
  os_type         = "Linux"
  image_publisher = "Canonical"
  image_offer     = "0001-com-ubuntu-server-jammy"
  image_sku       = "22_04-lts-gen2"
  
  location = var.azure_location
  vm_size  = var.vm_size
  
  ssh_username = var.ssh_username
  
  azure_tags = {
    Name        = "${var.image_name_prefix}-${local.timestamp}"
    Environment = "production"
    Builder     = "Packer"
    OS          = "Ubuntu 22.04"
  }
}

build {
  name = "tcb-app-azure-image"
  sources = [
    "source.azure-arm.ubuntu"
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
  
  # Azure requires this for generalization
  provisioner "shell" {
    execute_command = "chmod +x {{ .Path }}; {{ .Vars }} sudo -E sh '{{ .Path }}'"
    inline = [
      "/usr/sbin/waagent -force -deprovision+user && export HISTSIZE=0 && sync"
    ]
    inline_shebang = "/bin/sh -x"
  }
}
