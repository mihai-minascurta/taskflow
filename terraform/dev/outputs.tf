
output "vpc_id" {
  value = module.networking.vpc_id
}

output "database_endpoint" {
  value = module.rds.database_endpoint
}
