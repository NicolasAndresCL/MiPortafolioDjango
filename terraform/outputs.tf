output "api_public_ip" {
  description = "IP pública de la instancia de la API"
  value       = aws_instance.api.public_ip
}

output "api_url" {
  description = "URL de la API"
  value       = "http://${aws_instance.api.public_ip}:8000"
}

output "rds_endpoint" {
  description = "Endpoint de la base de datos RDS"
  value       = aws_db_instance.postgres.address
}
