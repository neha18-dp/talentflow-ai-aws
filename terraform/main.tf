resource "aws_vpc" "talentflow" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name        = "${var.project_name}-VPC"
    Environment = var.environment
  }
}

resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.talentflow.id
  cidr_block              = "172.31.1.0/24"
  availability_zone       = "${var.aws_region}a"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-Public-Subnet-A"
  }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.talentflow.id
  cidr_block              = "172.31.2.0/24"
  availability_zone       = "${var.aws_region}b"
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project_name}-Public-Subnet-B"
  }
}

resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.talentflow.id
  cidr_block        = "172.31.10.0/24"
  availability_zone = "${var.aws_region}a"

  tags = {
    Name = "${var.project_name}-Private-Subnet-A"
  }
}

resource "aws_subnet" "private_b" {
  vpc_id            = aws_vpc.talentflow.id
  cidr_block        = "172.31.20.0/24"
  availability_zone = "${var.aws_region}b"

  tags = {
    Name = "${var.project_name}-Private-Subnet-B"
  }
}

resource "aws_security_group" "application" {
  name        = "${var.project_name}-App-SG"
  description = "Security group for TalentFlow application"
  vpc_id      = aws_vpc.talentflow.id

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Application port from load balancer"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${var.project_name}-App-SG"
  }
}

resource "aws_s3_bucket" "talentflow" {
  bucket = "${lower(var.project_name)}-${lower(var.environment)}-storage"

  tags = {
    Name        = "${var.project_name}-S3"
    Environment = var.environment
  }
}

resource "aws_sqs_queue" "resume_queue" {
  name = "${lower(var.project_name)}-resume-queue"

  tags = {
    Name = "${var.project_name}-Resume-Queue"
  }
}

resource "aws_sns_topic" "notifications" {
  name = "${lower(var.project_name)}-notifications"

  tags = {
    Name = "${var.project_name}-Notifications"
  }
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${lower(var.project_name)}-resume-processor"
  retention_in_days = 14

  tags = {
    Name = "${var.project_name}-Lambda-Logs"
  }
}
