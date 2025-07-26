# Terraform configuration for Tuttino project infrastructure
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

# Volume persistente para PostgreSQL
resource "docker_volume" "pgdata" {
  name = "pgdata"
}

# Rede Docker interna
resource "docker_network" "tuttino_net" {
  name = "tuttino_net"
}

### Imagem do PostgreSQL
resource "docker_image" "postgres" {
  name = "postgres:15-alpine"
}
#### Imagem do PostgreSQL

### PostgreSQL container configuration
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

  cpu_shares = 512
  memory     = 4096
  restart    = "unless-stopped"
}
### PostgreSQL containerconfiguration


### Imagem do backend (FastAPI)
resource "docker_image" "backend" {
  name = "tuttino-backend:latest" 
  build {
    context    = abspath("${path.module}/../backend")
    dockerfile = "dockerfile"
  }
}
### Imagem do backend (FastAPI)


### Backend container configuration(FastAPI)
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

  cpu_shares = 256
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
### Backend container configuration(FastAPI)


### Imagem do Nginx
resource "docker_image" "nginx" {
  name = "nginx:latest"
  build {
    context    = abspath("${path.module}/../backend")
    dockerfile = "dockerfile"
  }
}
### Imagem do Nginx


### Nginx reverse proxy container configuration
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

volumes {
  host_path      = abspath("${path.module}/../nginx/conf.d")
  container_path = "/etc/nginx/conf.d"
}

  cpu_shares = 128
  memory     = 256
  restart    = "always"
}
### Nginx reverse proxy container configuration