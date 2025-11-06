# Azure Terraform Outputs

output "resource_group_name" {
  description = "Resource group name"
  value       = azurerm_resource_group.main.name
}

output "vm_id" {
  description = "Virtual machine ID"
  value       = azurerm_linux_virtual_machine.app.id
}

output "public_ip" {
  description = "Public IP address"
  value       = azurerm_public_ip.app.ip_address
}

output "public_fqdn" {
  description = "Public FQDN"
  value       = azurerm_public_ip.app.fqdn
}

output "vm_name" {
  description = "Virtual machine name"
  value       = azurerm_linux_virtual_machine.app.name
}

output "db_fqdn" {
  description = "PostgreSQL database FQDN"
  value       = var.use_postgresql ? azurerm_postgresql_flexible_server.main[0].fqdn : null
}

output "db_name" {
  description = "Database name"
  value       = var.use_postgresql ? var.db_name : null
}

output "app_url" {
  description = "Application URL"
  value       = "http://${azurerm_public_ip.app.ip_address}"
}
