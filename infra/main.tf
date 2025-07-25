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

resource "null_resource" "remove_old_backend" {
  provisioner "local-exec" {
    command = "docker rm -f tuttino-backend || true"
  }
}

resource "null_resource" "backend_build_trigger" {
  # Sempre que algum desses arquivos mudar, o hash muda e força o rebuild
  triggers = {
   always_run = timestamp()
  }
}

resource "docker_image" "backend" {
  name = "tuttino-backend:latest"

  build {
    context    = abspath("${path.module}/../backend")
    dockerfile = "dockerfile"
  }

  depends_on = [
    null_resource.backend_build_trigger,
    null_resource.remove_old_backend_image
  ]
}

resource "docker_container" "backend" {
  depends_on = [
    docker_container.postgres,
    null_resource.remove_old_backend
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

  restart = "always"
}

resource "null_resource" "remove_old_nginx" {
  provisioner "local-exec" {
    command = "docker rm -f tuttino-nginx || true"
  }
}

resource "docker_image" "nginx" {
  name = "nginx:stable-alpine"
}

resource "docker_container" "nginx" {
  depends_on = [
    docker_container.backend,
    null_resource.remove_old_nginx
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

  restart = "always"
}

resource "null_resource" "remove_old_backend_image" {
  provisioner "local-exec" {
    command = "docker rmi -f tuttino-backend:latest || true"
  }
  depends_on = [null_resource.remove_old_backend]
}
