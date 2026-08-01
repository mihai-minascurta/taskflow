variable "vpc_id" {
  description = "VPC where RDS will be deployed"
  type        = string
}


variable "private_subnet_ids" {
  description = "Private subnet IDs for RDS"
  type        = list(string)
}


variable "eks_security_group_id" {
  description = "Security group allowed to access RDS"
  type        = string
}


variable "database_name" {
  description = "Initial database name"
  type        = string
  default     = "taskflow"
}


variable "database_username" {
  description = "Database master username"
  type        = string
  default     = "taskflow_admin"
}


variable "database_password" {
  description = "Database password"
  type        = string
  sensitive   = true
}