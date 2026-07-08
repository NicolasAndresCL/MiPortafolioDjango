variable "aws_region" {
  description = "Región de AWS"
  type        = string
  default     = "us-east-1"
}

variable "instance_type" {
  description = "Tipo de instancia EC2 para la API"
  type        = string
  default     = "t3.micro"
}

variable "db_instance_class" {
  description = "Clase de instancia RDS"
  type        = string
  default     = "db.t3.micro"
}

variable "ami_id" {
  description = "AMI base (Ubuntu 22.04 LTS con soporte cloud-init)"
  type        = string
}

variable "key_name" {
  description = "Nombre del key pair EC2 para acceso SSH"
  type        = string
}

variable "ssh_cidr" {
  description = "CIDR autorizado para SSH"
  type        = string
  default     = "0.0.0.0/0"
}

variable "db_username" {
  description = "Usuario de Postgres"
  type        = string
  default     = "portafolio"
}

variable "db_password" {
  description = "Password de Postgres"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "SECRET_KEY de Django para la app"
  type        = string
  sensitive   = true
}

variable "allowed_hosts" {
  description = "ALLOWED_HOSTS (CSV) para Django"
  type        = string
  default     = "*"
}

variable "image" {
  description = "Imagen del contenedor a desplegar"
  type        = string
  default     = "ghcr.io/nicolasandrescl/portafolio-backend:latest"
}
