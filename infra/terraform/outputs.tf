output "db_endpoint"   { value = module.rds.db_instance_endpoint }
output "db_name"       { value = module.rds.db_instance_name }
output "ecr_gateway"   { value = aws_ecr_repository.gateway.repository_url }
output "ecr_forecast"  { value = aws_ecr_repository.forecast.repository_url }
output "ecr_dashboard" { value = aws_ecr_repository.dashboard.repository_url }
