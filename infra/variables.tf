variable "env" {
  description = "Ambiente de deploy (ex: dev, prod, staging)"
  type        = string
  default     = "dev"
}

variable "db_user" {
  type    = string
  default = "tuttino_user"
}

variable "db_pass" {
  type    = string
  default = "tuttino_pass"
}

variable "db_name" {
  type    = string
  default = "tuttino_db"
}

variable "nginx_port" {
  description = "Porta externa para o Nginx"
  type        = number
  default     = 80
}

variable "backend_port" {
  description = "Porta externa para o backend"
  type        = number
  default     = 8000
}

variable "nginx_image" {
  description = "Imagem do Nginx"
  type        = string
  default     = "tuttino-nginx:latest"
}

variable "backend_image" {
  description = "Imagem do backend"
  type        = string
  default     = "tuttino-backend:latest"
}

variable "postgres_image" {
  description = "Imagem do PostgreSQL"
  type        = string
  default     = "postgres:15-alpine"
}

variable "postgres_version" {
  description = "Versão do PostgreSQL"
  type        = string
  default     = "15-alpine"
}

# Agora com base no ambiente
variable "docker_network_name" {
  description = "Nome da rede Docker compartilhada entre os containers"
  type        = string
  default     = ""
}

variable "docker_volume_name" {
  description = "Nome do volume Docker persistente para o PostgreSQL"
  type        = string
  default     = ""
}
