data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "pod_identity_assume_role" {
  statement {
    sid    = "AllowEksPodIdentity"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["pods.eks.amazonaws.com"]
    }

    actions = [
      "sts:AssumeRole",
      "sts:TagSession",
    ]
  }
}

#
# App roles: split prod/default and staging for least privilege
#

data "aws_iam_policy_document" "cloud_task_api_prod_secrets_read" {
  statement {
    sid    = "ReadProdSecrets"
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
    ]

    resources = [
      "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:cloud-task-api/prod/django*",
      "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:cloud-task-api/prod/postgres*",
    ]
  }
}

data "aws_iam_policy_document" "cloud_task_api_staging_secrets_read" {
  statement {
    sid    = "ReadStagingSecrets"
    effect = "Allow"
    actions = [
      "secretsmanager:GetSecretValue",
      "secretsmanager:DescribeSecret",
    ]

    resources = [
      "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:cloud-task-api/staging/django*",
      "arn:aws:secretsmanager:${var.aws_region}:${data.aws_caller_identity.current.account_id}:secret:cloud-task-api/staging/postgres*",
    ]
  }
}

resource "aws_iam_role" "cloud_task_api_prod_secrets" {
  name               = "CloudTaskApiProdSecretsRole"
  assume_role_policy = data.aws_iam_policy_document.pod_identity_assume_role.json

  tags = {
    Project = var.cluster_name
    Managed = "terraform"
    Env     = "prod"
  }
}

resource "aws_iam_role" "cloud_task_api_staging_secrets" {
  name               = "CloudTaskApiStagingSecretsRole"
  assume_role_policy = data.aws_iam_policy_document.pod_identity_assume_role.json

  tags = {
    Project = var.cluster_name
    Managed = "terraform"
    Env     = "staging"
  }
}

resource "aws_iam_policy" "cloud_task_api_prod_secrets_read" {
  name   = "CloudTaskApiProdSecretsReadPolicy"
  policy = data.aws_iam_policy_document.cloud_task_api_prod_secrets_read.json
}

resource "aws_iam_policy" "cloud_task_api_staging_secrets_read" {
  name   = "CloudTaskApiStagingSecretsReadPolicy"
  policy = data.aws_iam_policy_document.cloud_task_api_staging_secrets_read.json
}

resource "aws_iam_role_policy_attachment" "cloud_task_api_prod_secrets_read" {
  role       = aws_iam_role.cloud_task_api_prod_secrets.name
  policy_arn = aws_iam_policy.cloud_task_api_prod_secrets_read.arn
}

resource "aws_iam_role_policy_attachment" "cloud_task_api_staging_secrets_read" {
  role       = aws_iam_role.cloud_task_api_staging_secrets.name
  policy_arn = aws_iam_policy.cloud_task_api_staging_secrets_read.arn
}

resource "aws_eks_pod_identity_association" "cloud_task_api_default" {
  cluster_name    = module.eks.cluster_name
  namespace       = "default"
  service_account = "cloud-task-api-sa"
  role_arn        = aws_iam_role.cloud_task_api_prod_secrets.arn

  tags = {
    Managed = "terraform"
    App     = "cloud-task-api"
    Env     = "prod"
  }
}

resource "aws_eks_pod_identity_association" "cloud_task_api_staging" {
  cluster_name    = module.eks.cluster_name
  namespace       = "staging"
  service_account = "cloud-task-api-sa"
  role_arn        = aws_iam_role.cloud_task_api_staging_secrets.arn

  tags = {
    Managed = "terraform"
    App     = "cloud-task-api"
    Env     = "staging"
  }
}


#
# CloudWatch agent role + association
#

resource "aws_iam_role" "cloudwatch_observability" {
  name               = "AmazonEKSCloudWatchObservabilityRole"
  assume_role_policy = data.aws_iam_policy_document.pod_identity_assume_role.json

  tags = {
    Project = var.cluster_name
    Managed = "terraform"
    App     = "amazon-cloudwatch"
  }
}

resource "aws_iam_role_policy_attachment" "cloudwatch_agent_server" {
  role       = aws_iam_role.cloudwatch_observability.name
  policy_arn = "arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy"
}

resource "aws_eks_pod_identity_association" "cloudwatch_agent" {
  cluster_name    = module.eks.cluster_name
  namespace       = "amazon-cloudwatch"
  service_account = "cloudwatch-agent"
  role_arn        = aws_iam_role.cloudwatch_observability.arn

  tags = {
    Managed = "terraform"
    App     = "cloudwatch-agent"
  }
}

output "cloud_task_api_prod_secrets_role_arn" {
  value = aws_iam_role.cloud_task_api_prod_secrets.arn
}

output "cloud_task_api_staging_secrets_role_arn" {
  value = aws_iam_role.cloud_task_api_staging_secrets.arn
}

output "cloudwatch_observability_role_arn" {
  value = aws_iam_role.cloudwatch_observability.arn
}