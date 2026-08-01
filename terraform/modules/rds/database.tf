resource "aws_db_instance" "this" {


  identifier = "taskflow-postgres"


  engine = "postgres"

  engine_version = "16"


  instance_class = "db.t3.micro"


  allocated_storage = 20


  storage_type = "gp3"



  db_name = var.database_name


  username = var.database_username


  password = var.database_password



  db_subnet_group_name = aws_db_subnet_group.this.name



  vpc_security_group_ids = [
    aws_security_group.this.id
  ]



  publicly_accessible = false



  backup_retention_period = 0



  storage_encrypted = true



  skip_final_snapshot = true



  tags = {

    Name = "taskflow-postgres"

  }

}