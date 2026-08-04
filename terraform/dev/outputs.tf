output "cluster_name" {
    value = module.cluster.cluster_name
}

output "vpc_id" {
  value = module.networking.vpc_id
}

output "database_endpoint" {
  value = module.rds.database_endpoint
}

output "alb_controller_role_arn" {

  value = module.alb_controller.alb_controller_role_arn

}
