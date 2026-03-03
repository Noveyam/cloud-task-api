variable "aws_region" {
    type = string
    default = "us-east-1"
}

#Must be globally unique across ALL AWS accounts
variable "state_bucket_name" {
    type = string
}

variable "lock_table_name" {
    type = string
    default = "noveyam-cloud-task-api-tflock"
}