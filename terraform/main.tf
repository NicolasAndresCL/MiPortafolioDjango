terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # State local por ahora. Roadmap: mover a backend remoto S3 + bloqueo DynamoDB.
  # backend "s3" {
  #   bucket         = "portafolio-tfstate"
  #   key            = "backend/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "portafolio-tflock"
  # }
}

provider "aws" {
  region = var.aws_region
}

# ─── Redes / seguridad ─────────────────────────────────────────────────────────

resource "aws_security_group" "api" {
  name        = "portafolio-api"
  description = "Portafolio backend API (HTTP + SSH)"

  ingress {
    description = "API HTTP"
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.ssh_cidr]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_security_group" "db" {
  name        = "portafolio-db"
  description = "Postgres accesible solo desde la API"

  ingress {
    description     = "Postgres desde la API"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.api.id]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ─── Base de datos gestionada (RDS Postgres) ───────────────────────────────────

resource "aws_db_instance" "postgres" {
  identifier             = "portafolio-db"
  engine                 = "postgres"
  engine_version         = "16"
  instance_class         = var.db_instance_class
  allocated_storage      = 20
  db_name                = "portafolio"
  username               = var.db_username
  password               = var.db_password
  vpc_security_group_ids = [aws_security_group.db.id]
  publicly_accessible    = false
  skip_final_snapshot    = true
}

# ─── Cómputo (EC2 corriendo el contenedor de GHCR) ─────────────────────────────

resource "aws_instance" "api" {
  ami                    = var.ami_id
  instance_type          = var.instance_type
  key_name               = var.key_name
  vpc_security_group_ids = [aws_security_group.api.id]

  user_data = templatefile("${path.module}/cloud-init.yaml", {
    image         = var.image
    secret_key    = var.secret_key
    allowed_hosts = var.allowed_hosts
    database_url  = "postgres://${var.db_username}:${var.db_password}@${aws_db_instance.postgres.address}:5432/portafolio"
  })

  tags = {
    Name    = "portafolio-api"
    Project = "portafolio"
  }
}
