provider "aws" {
  region = var.aws_region
}

data "aws_availability_zones" "available" {}

data "aws_route53_zone" "main" {
  name         = "noveycloud.com"
  private_zone = false
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = "${var.cluster_name}-vpc"
  cidr = var.vpc_cidr

  azs             = slice(data.aws_availability_zones.available.names, 0, 2)
  private_subnets = ["10.20.1.0/24", "10.20.2.0/24"]
  public_subnets  = ["10.20.101.0/24", "10.20.102.0/24"]

  enable_nat_gateway = true
  single_nat_gateway = true

  public_subnet_tags = {
    "kubernetes.io/role/elb"                    = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }

  private_subnet_tags = {
    "kubernetes.io/role/internal-elb"           = "1"
    "kubernetes.io/cluster/${var.cluster_name}" = "shared"
  }
}

module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 21.0"

  name               = var.cluster_name
  kubernetes_version = "1.35"

  authentication_mode                      = "API_AND_CONFIG_MAP"
  enable_cluster_creator_admin_permissions = true

  endpoint_public_access = true
  vpc_id                 = module.vpc.vpc_id
  subnet_ids             = module.vpc.private_subnets

  addons = {
    vpc-cni = {
      before_compute = true
      most_recent    = true
      preserve       = false
    }
    kube-proxy = {
      before_compute = true
      most_recent    = true
    }
    coredns = {
      before_compute = true
      most_recent    = true
    }
  }

  eks_managed_node_groups = {
    default = {
      instance_types = ["t3.medium"]
      min_size       = 2
      max_size       = 3
      desired_size   = 2
    }
  }
}
