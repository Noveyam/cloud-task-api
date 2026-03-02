data "aws_caller_identity" "current" {}

output "account_id" {
    value = data.aws_caller_identity.current.account_id
}

output "ec2_public_ip" {
    value = aws_instance.app.public_ip
}

output "ec2_public_dns" {
    value = aws_instance.app.public_dns
}

output "vpc_id" {
    value = aws_vpc.main.id
}
