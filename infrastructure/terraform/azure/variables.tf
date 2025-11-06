# Azure Terraform Variables

variable "location" {
  description = "Azure region to deploy resources"
  type        = string
  default     = "eastus"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "tcb-trading-card-brain"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "vnet_cidr" {
  description = "CIDR block for VNet"
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "CIDR block for subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "vm_size" {
  description = "Azure VM size"
  type        = string
  default     = "Standard_B2s"
}

variable "admin_username" {
  description = "Admin username for VM"
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key" {
  description = "SSH public key for VM access"
  type        = string
}

variable "use_postgresql" {
  description = "Whether to create PostgreSQL database"
  type        = bool
  default     = false
}

variable "db_sku_name" {
  description = "PostgreSQL SKU name"
  type        = string
  default     = "B_Standard_B1ms"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "tcb_db"
}

variable "db_username" {
  description = "Database admin username"
  type        = string
  default     = "tcbadmin"
}

variable "db_password" {
  description = "Database admin password"
  type        = string
  sensitive   = true
}
