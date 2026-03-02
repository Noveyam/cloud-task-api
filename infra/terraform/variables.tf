variable "project_name" {
    type = string
    default = "cloud-task-api"
}

variable "aws_region" {
    type = string
    default = "us-east-1"
}

variable "vpc_cidr" {
    type = string
    default = "10.0.0.0/16"
}

variable "public_subnet_cidr" {
    type = string
    default = "10.0.1.0/24"
}

variable "instance_type" {
    type = string
    default = "t3.micro"
}

#Must match EC2 Key Pair name
variable "key_name" {
    type = string
}

#Public IP in CIDR form
variable "ssh_cidr" {
    type = string
}