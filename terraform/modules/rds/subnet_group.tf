resource "aws_db_subnet_group" "this" {

  name = "taskflow-db-subnet-group"


  subnet_ids = var.private_subnet_ids


  tags = {
    Name = "taskflow-rds-subnet-group"
  }

}