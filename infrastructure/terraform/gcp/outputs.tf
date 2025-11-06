# GCP Terraform Outputs

output "instance_name" {
  description = "Compute instance name"
  value       = google_compute_instance.app.name
}

output "instance_id" {
  description = "Compute instance ID"
  value       = google_compute_instance.app.id
}

output "public_ip" {
  description = "Public IP address"
  value       = google_compute_address.app.address
}

output "network_name" {
  description = "VPC network name"
  value       = google_compute_network.main.name
}

output "db_connection_name" {
  description = "Cloud SQL connection name"
  value       = var.use_cloud_sql ? google_sql_database_instance.main[0].connection_name : null
}

output "db_ip_address" {
  description = "Cloud SQL IP address"
  value       = var.use_cloud_sql ? google_sql_database_instance.main[0].ip_address[0].ip_address : null
}

output "db_name" {
  description = "Database name"
  value       = var.use_cloud_sql ? var.db_name : null
}

output "app_url" {
  description = "Application URL"
  value       = "http://${google_compute_address.app.address}"
}
