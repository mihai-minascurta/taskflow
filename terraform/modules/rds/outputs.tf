output "database_endpoint" {

  description = "RDS endpoint"

  value = aws_db_instance.this.address

}


output "database_port" {

  description = "Database port"

  value = aws_db_instance.this.port

}


output "database_name" {

  value = aws_db_instance.this.db_name

}