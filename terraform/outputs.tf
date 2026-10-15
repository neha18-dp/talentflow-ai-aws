output "vpc_id" {
  description = "TalentFlow VPC ID"
  value       = aws_vpc.talentflow.id
}

output "public_subnet_a_id" {
  description = "Public subnet A ID"
  value       = aws_subnet.public_a.id
}

output "public_subnet_b_id" {
  description = "Public subnet B ID"
  value       = aws_subnet.public_b.id
}

output "private_subnet_a_id" {
  description = "Private subnet A ID"
  value       = aws_subnet.private_a.id
}

output "private_subnet_b_id" {
  description = "Private subnet B ID"
  value       = aws_subnet.private_b.id
}

output "s3_bucket_name" {
  description = "TalentFlow S3 bucket name"
  value       = aws_s3_bucket.talentflow.bucket
}

output "sqs_queue_url" {
  description = "TalentFlow SQS queue URL"
  value       = aws_sqs_queue.resume_queue.url
}

output "sns_topic_arn" {
  description = "TalentFlow SNS topic ARN"
  value       = aws_sns_topic.notifications.arn
}

output "lambda_log_group" {
  description = "Lambda CloudWatch log group"
  value       = aws_cloudwatch_log_group.lambda.name
}
