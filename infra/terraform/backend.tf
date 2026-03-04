terraform {
  backend "s3" {
    bucket         = "noveyam-cloud-task-api-tfstate-001"
    key            = "cloud-task-api/dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "noveyam-cloud-task-api-tflock"
    encrypt        = true
  }
}