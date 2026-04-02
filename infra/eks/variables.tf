variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "cluster_name" {
  type    = string
  default = "cloud-task-api-eks"
}

variable "vpc_cidr" {
  type    = string
  default = "10.20.0.0/16"
}
