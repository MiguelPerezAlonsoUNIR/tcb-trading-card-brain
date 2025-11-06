# GCP Terraform Configuration for TCB Trading Card Brain

terraform {
  required_version = ">= 1.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# VPC Network
resource "google_compute_network" "main" {
  name                    = "${var.project_name}-network"
  auto_create_subnetworks = false
}

# Subnet
resource "google_compute_subnetwork" "app" {
  name          = "${var.project_name}-app-subnet"
  ip_cidr_range = var.subnet_cidr
  region        = var.region
  network       = google_compute_network.main.id
}

# Firewall Rules
resource "google_compute_firewall" "ssh" {
  name    = "${var.project_name}-allow-ssh"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = var.ssh_allowed_ips
  target_tags   = ["${var.project_name}-app"]
}

resource "google_compute_firewall" "http" {
  name    = "${var.project_name}-allow-http"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["80", "443"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["${var.project_name}-app"]
}

resource "google_compute_firewall" "flask" {
  name    = "${var.project_name}-allow-flask"
  network = google_compute_network.main.name

  allow {
    protocol = "tcp"
    ports    = ["5000"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["${var.project_name}-app"]
}

# Static IP
resource "google_compute_address" "app" {
  name   = "${var.project_name}-app-ip"
  region = var.region
}

# Compute Instance
resource "google_compute_instance" "app" {
  name         = "${var.project_name}-app-vm"
  machine_type = var.machine_type
  zone         = var.zone

  tags = ["${var.project_name}-app"]

  boot_disk {
    initialize_params {
      image = var.image_id != "" ? var.image_id : "ubuntu-os-cloud/ubuntu-2204-lts"
      size  = 30
      type  = "pd-standard"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.app.id

    access_config {
      nat_ip = google_compute_address.app.address
    }
  }

  metadata = {
    ssh-keys = "${var.ssh_username}:${var.ssh_public_key}"
  }

  metadata_startup_script = templatefile("${path.module}/user-data.sh", {
    environment = var.environment
  })

  labels = {
    environment = var.environment
    project     = var.project_name
  }
}

# Cloud SQL PostgreSQL Instance (Optional)
resource "google_sql_database_instance" "main" {
  count            = var.use_cloud_sql ? 1 : 0
  name             = "${var.project_name}-db-${var.environment}"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier = var.db_tier

    ip_configuration {
      ipv4_enabled = true
      authorized_networks {
        name  = "app-vm"
        value = google_compute_address.app.address
      }
    }

    backup_configuration {
      enabled = true
    }
  }

  deletion_protection = false
}

resource "google_sql_database" "main" {
  count    = var.use_cloud_sql ? 1 : 0
  name     = var.db_name
  instance = google_sql_database_instance.main[0].name
}

resource "google_sql_user" "main" {
  count    = var.use_cloud_sql ? 1 : 0
  name     = var.db_username
  instance = google_sql_database_instance.main[0].name
  password = var.db_password
}
