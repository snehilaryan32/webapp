variable "project_id" {
  type    = string
  default = "csye6225-414117"
}

variable "source_image_family" {
  type    = string
  default = "centos-8"
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


packer {
  required_plugins {
    googlecompute = {
      version = ">= 0.0.2"
      source  = "github.com/hashicorp/googlecompute"
    }
  }
}

source "googlecompute" "flask-app-image" {
  project_id = var.project_id
  source_image_family = var.source_image_family
  ssh_username = var.ssh_username
  zone = var.zone
  instance_name = var.instance_name
  image_name = var.image_name
  machine_type = var.machine_type
}

