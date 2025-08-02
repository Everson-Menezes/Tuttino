###### Terraform configuration for Tuttino project infrastructure ###### 
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

###### Volume persistente para PostgreSQL ###### 
resource "docker_volume" "pgdata" {
  name = "pgdata"
}

###### Rede Docker interna ###### 
resource "docker_network" "tuttino_net" {
  name = "tuttino_net"
}

###### Imagem do PostgreSQL ###### 
resource "docker_image" "postgres" {
  name = "postgres:15-alpine"
}

###### Container PostgreSQL ###### 
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
  cpu_shares = 1024 ###### 1 vCPU ###### PostgreSQL é o serviço mais pesado, então aloquei 1 vCPU
  # PostgreSQL pode consumir mais memória dependendo da carga, mas 4GB é um
  # valor razoável para a maioria dos casos de uso.
  memory     = 4096
  restart    = "unless-stopped"
}

###### Imagem do backend (FastAPI) ###### 
resource "docker_image" "backend" {
  name = "tuttino-backend:latest"
  build {
    context    = abspath("${path.module}/../backend")
    dockerfile = "dockerfile"
  }
}

###### Container Backend (FastAPI) ###### 
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

  cpu_shares = 768 ###### 0.75 vCPU ###### FastAPI é mais pesado que o Nginx, mas não tanto quanto o PostgreSQL
  # O FastAPI pode consumir mais memória dependendo da carga, mas 2GB é um
  # valor razoável para a maioria dos casos de uso.
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

###### Imagem do Nginx ###### 
resource "docker_image" "nginx" {
  name = "tuttino-nginx:latest"
  build {
    context    = abspath("${path.module}/../nginx")
    dockerfile = "dockerfile"
  }
}

###### Container Nginx ###### 
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
  cpu_shares = 256 ###### 0.25 vCPU ###### Nginx é leve e não precisa de muito poder de CPU
  memory     = 256
  restart    = "always"
}