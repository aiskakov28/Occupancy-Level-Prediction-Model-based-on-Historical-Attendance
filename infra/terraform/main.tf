terraform {
  required_version = ">= 1.5.0"
  required_providers { aws = { source = "hashicorp/aws" version = "~> 5.0" } }
}
provider "aws" { region = var.region }
data "aws_availability_zones" "available" {}
locals { name = var.project }

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.1.2"
  name = "${local.name}-vpc"
  cidr = "10.0.0.0/16"
  azs  = slice(data.aws_availability_zones.available.names, 0, 2)
  private_subnets = ["10.0.1.0/24","10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24","10.0.102.0/24"]
  enable_nat_gateway = true
  single_nat_gateway = true
}

module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.6.0"
  identifier = "${local.name}-pg"
  engine = "postgres"
  engine_version = "15.5"
  family = "postgres15"
  instance_class = "db.t4g.micro"
  allocated_storage = 20
  db_name = "occupancy"
  username = var.db_user
  password = var.db_password
  port = 5432
  publicly_accessible = true
  vpc_security_group_ids = [module.vpc.default_security_group_id]
  subnet_ids = module.vpc.public_subnets
  skip_final_snapshot = true
}

resource "aws_ecr_repository" "gateway"  { name = "${local.name}-gateway" }
resource "aws_ecr_repository" "forecast" { name = "${local.name}-forecast" }
resource "aws_ecr_repository" "dashboard"{ name = "${local.name}-dashboard" }
