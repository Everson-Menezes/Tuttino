terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.2"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

resource "docker_network" "tuttino_net" {
  name = "tuttino_net"
}

resource "docker_volume" "pgdata" {
  name = "tuttino_pgdata"
}

resource "docker_image" "postgres" {
  name = "postgres:15-alpine"
}

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
}

resource "docker_image" "backend" {
  name = "tuttino-backend:latest"
  build {
    context = abspath("${path.module}/../backend")
  }
}

resource "docker_container" "backend" {
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

  depends_on = [docker_container.postgres]

  ports {
    internal = 8000
    external = 8000
  }

  volumes {
    host_path      = abspath("${path.module}/../backend")
    container_path = "/app"
  }
}

resource "docker_image" "nginx" {
  name = "nginx:stable-alpine"
}

resource "docker_container" "nginx" {
  name  = "tuttino-nginx"
  image = docker_image.nginx.name

  networks_advanced {
    name = docker_network.tuttino_net.name
  }

  depends_on = [docker_container.backend]

  ports {
    internal = 80
    external = 80
  }

  volumes {
    host_path      = abspath("${path.module}/../nginx/conf.d")
    container_path = "/etc/nginx/conf.d"
  }
}