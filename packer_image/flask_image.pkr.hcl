variable "project_id" {
  type    = string
  default = "csye6225-414117"
}

variable "source_image_family" {
  type    = string
  default = "centos-stream-8"
}

variable "ssh_username" {
  type    = string
  default = "packer"
}

variable "zone" {
  type    = string
  default = "us-central1-a"
}

variable "image_name" {
  type    = string
  default = "flask-app"
}

variable "instance_name" {
  type    = string
  default = "flask-image-builder"
}

variable "machine_type" {
  type    = string
  default = "f1-micro"
}

variable "db_name" {
  description = "The name of the database"
  default     = "firstdb"
}

variable "db_user" {
  description = "The database username"
}

variable "db_pass" {
  description = "The database password"
}

variable "db_host" {
  description = "The database host"
  default     = "localhost"
}

variable "db_port" {
  description = "The database port"
  default     = 5432
}


packer {
  required_plugins {
    googlecompute = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/googlecompute"
    }
  }
}

source "googlecompute" "flask-app-image" {
  project_id            = var.project_id
  source_image_family     = var.source_image_family
  ssh_username          = var.ssh_username
  zone                = var.zone
  instance_name       = var.instance_name
  image_name          = var.image_name
}

build {
  sources = ["source.googlecompute.flask-app-image"]

  provisioner "file" {
    source      = "./flask-app.zip"
    destination = "/home/${var.ssh_username}/"
  }

  provisioner "file" {
    source      = "./flaskapp.service"
    destination = "/home/${var.ssh_username}/"
  }

  provisioner "shell" {
    script = "./install_dependencies.sh"
  }

  provisioner "shell" {
    script = "./setup_postgres.sh"
    environment_vars = [
      "DB_NAME=${var.db_name}",
      "DB_USER=${var.db_user}",
      "DB_PASS=${var.db_pass}"
    ]
  }

  provisioner "shell" {
    script = "./setup_flask_app.sh"
    environment_vars = [
      "DB_NAME=${var.db_name}",
      "DB_USER=${var.db_user}",
      "DB_PASS=${var.db_pass}"
    ]
  }

  provisioner "shell" {
    script = "./generate_env_file.sh"
    environment_vars = [
      "DB_HOST=${var.db_host}",
      "DB_PORT=${var.db_port}",
      "DB_NAME=${var.db_name}",
      "DB_USER=${var.db_user}",
      "DB_PASSWORD=${var.db_pass}"
    ]
  }

  provisioner "shell" {
    script = "./setup_service.sh"
  }
}

