### Terraform configuration for Tuttino project infrastructure ###
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

### Persistent volume for PostgreSQL ###
resource "docker_volume" "pgdata" {
  name = "pgdata"
}

### Docker internal network (shared between containers) ###
resource "docker_network" "tuttino_net" {
  name = "tuttino_net"

  lifecycle {
    ignore_changes   = all
    prevent_destroy  = true
  }
}

### PostgreSQL image (lightweight version based on Alpine) ###
resource "docker_image" "postgres" {
  name = "postgres:15-alpine"
}

### PostgreSQL container ###
resource "docker_container" "postgres" {
  name  = "tuttino-postgres"
  image = docker_image.postgres.name

  env = [
    "POSTGRES_USER=${var.db_user}",
    "POSTGRES_PASSWORD=${var.db_pass}",
    "POSTGRES_DB=${var.db_name}"
  ]

  volumes {
    volume_name    = docker_volume.pgdata.name
    container_path = "/var/lib/postgresql/data"
  }

  networks_advanced {
    name = docker_network.tuttino_net.name
  }

  ports {
    internal = 5432
    external = 5432
  }

  # PostgreSQL is the heaviest service — allocate 1 vCPU and 4GB RAM
  cpu_shares = 1024
  memory     = 4096
  restart    = "unless-stopped"
}

### Backend image (FastAPI) ###
resource "docker_image" "backend" {
  name = "tuttino-backend:latest"
  build {
    context    = abspath("${path.module}/../backend")
    dockerfile = "dockerfile"  # tudo minúsculo, conforme seu arquivo
  }
}


### Backend container (FastAPI) ###
resource "docker_container" "backend" {
  depends_on = [
    docker_container.postgres
  ]

  name  = "tuttino-backend"
  image = docker_image.backend.name

  env = [
    "DB_HOST=tuttino-postgres",
    "DB_PORT=5432",
    "DB_NAME=${var.db_name}",
    "DB_USER=${var.db_user}",
    "DB_PASS=${var.db_pass}"
  ]

  networks_advanced {
    name = docker_network.tuttino_net.name
  }

  ports {
    internal = 8000
    external = 8000
  }

  volumes {
    host_path      = abspath("${path.module}/../backend")
    container_path = "/backend"
  }

  # Allocate 0.75 vCPU and 2GB RAM for backend
  cpu_shares = 768
  memory     = 2048
  restart    = "always"

  command = [
    "uvicorn",
    "main:app",
    "--host", "0.0.0.0",
    "--port", "8000",
    "--workers", "4"
  ]
}

### Nginx image ###
resource "docker_image" "nginx" {
  name = "tuttino-nginx:latest"
  build {
    context    = abspath("${path.module}/../infra/nginx")
    dockerfile = "dockerfile"  # tudo minúsculo também
  }
}


### Nginx container ###
resource "docker_container" "nginx" {
  depends_on = [
    docker_container.backend
  ]

  name  = "tuttino-nginx"
  image = docker_image.nginx.name

  networks_advanced {
    name = docker_network.tuttino_net.name
  }

  ports {
    internal = 80
    external = 80
  }

  # Lightweight proxy, 0.25 vCPU and 256MB RAM
  cpu_shares = 256
  memory     = 256
  restart    = "always"
}
