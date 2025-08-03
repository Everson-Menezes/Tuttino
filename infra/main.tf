terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

### Tuttino network (shared between containers) ###
resource "docker_network" "tuttino_net" {
  name = var.docker_network_name != "" ? var.docker_network_name : "tuttino-${var.env}-net"

  lifecycle {
    prevent_destroy = true
  }
}

### Persistent volume for PostgreSQL ###
resource "docker_volume" "pgdata" {
  name = var.docker_volume_name != "" ? var.docker_volume_name : "pgdata-${var.env}"
}

### PostgreSQL image (lightweight version based on Alpine) ###
resource "docker_image" "postgres" {
  name = var.postgres_image
}

### PostgreSQL container ###
resource "docker_container" "postgres" {
  name  = "tuttino-postgres-${var.env}"
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
    name = "tuttino-dev-net" # ou "tuttino_net" se quiser o nome fixo
  }

  ports {
    internal = 5432
    external = 5432
  }

  cpu_shares = 1024
  memory     = 4096
  restart    = "unless-stopped"
}

### Backend image (FastAPI) ###
resource "docker_image" "backend" {
  name         = "tuttino-backend"
  keep_locally = false

  build {
    context    = abspath("${path.module}/../backend")
    dockerfile = "dockerfile_back"
  }
}

### Backend container (FastAPI) ###
resource "docker_container" "backend" {
  depends_on = [
    docker_container.postgres
  ]

  name  = "tuttino-backend-${var.env}"
  image = docker_image.backend.name

  env = [
    "DB_HOST=tuttino-postgres-${var.env}",
    "DB_PORT=5432",
    "DB_NAME=${var.db_name}",
    "DB_USER=${var.db_user}",
    "DB_PASS=${var.db_pass}"
  ]

  networks_advanced {
    name = "tuttino-dev-net"
  }

  ports {
    internal = 8000
    external = var.backend_port
  }

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
  name         = var.nginx_image
  build {
    context    = abspath("${path.module}/nginx")
    dockerfile = "dockerfile_infra"
  }
}

### Nginx container ###
resource "docker_container" "nginx" {
  depends_on = [
    docker_container.backend
  ]

  name  = "tuttino-nginx-${var.env}"
  image = docker_image.nginx.name

  networks_advanced {
    name = "tuttino-dev-net"
  }

  ports {
    internal = 80
    external = var.nginx_port
  }

  cpu_shares = 256
  memory     = 256
  restart    = "always"
}
