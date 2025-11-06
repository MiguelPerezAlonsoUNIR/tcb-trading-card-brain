# GCP Terraform Variables

variable "project_id" {
  description = "GCP project ID"
  type        = string
}

variable "region" {
  description = "GCP region to deploy resources"
  type        = string
  default     = "us-east1"
}

variable "zone" {
  description = "GCP zone to deploy resources"
  type        = string
  default     = "us-east1-b"
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

variable "subnet_cidr" {
  description = "CIDR block for subnet"
  type        = string
  default     = "10.0.1.0/24"
}

variable "machine_type" {
  description = "GCP machine type"
  type        = string
  default     = "e2-small"
}

variable "image_id" {
  description = "Custom image ID (optional)"
  type        = string
  default     = ""
}

variable "ssh_username" {
  description = "SSH username"
  type        = string
  default     = "gcpuser"
}

variable "ssh_public_key" {
  description = "SSH public key"
  type        = string
}

variable "ssh_allowed_ips" {
  description = "List of IP addresses allowed to SSH"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}

variable "use_cloud_sql" {
  description = "Whether to create Cloud SQL database"
  type        = bool
  default     = false
}

variable "db_tier" {
  description = "Cloud SQL tier"
  type        = string
  default     = "db-f1-micro"
}

variable "db_name" {
  description = "Database name"
  type        = string
  default     = "tcb_db"
}

variable "db_username" {
  description = "Database username"
  type        = string
  default     = "tcbadmin"
}

variable "db_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}
