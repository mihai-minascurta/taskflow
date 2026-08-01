output "vpc_id" {
  value = aws_vpc.main_vpc.id
}

output "public_subnet_a_id" {
    value = aws_subnet.public_a_subnet.id
  
}

output "public_subnet_b_id" {
    value = aws_subnet.public_b_subnet.id
  
}

output "private_subnet_a_id" {
    value = aws_subnet.private_a_subnet.id
  
}

output "private_subnet_b_id" {
    value = aws_subnet.private_b_subnet.id
  
}