# AWS Terraform Outputs

output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.app.id
}

output "public_ip" {
  description = "Public IP address"
  value       = aws_eip.app.public_ip
}

output "public_dns" {
  description = "Public DNS name"
  value       = aws_instance.app.public_dns
}

output "security_group_id" {
  description = "Security group ID"
  value       = aws_security_group.app.id
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "db_endpoint" {
  description = "RDS database endpoint"
  value       = var.use_rds ? aws_db_instance.main[0].endpoint : null
}

output "db_name" {
  description = "Database name"
  value       = var.use_rds ? var.db_name : null
}

output "app_url" {
  description = "Application URL"
  value       = "http://${aws_eip.app.public_ip}"
}
