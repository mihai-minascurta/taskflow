resource "aws_vpc" "main_vpc" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = {
    Name = "Taskflow-VPC"
  }

}

resource "aws_subnet" "public_a_subnet" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "eu-central-1a"
  map_public_ip_on_launch = true

  tags = {
    Name                                  = "Public-Subnet-A"
    "kubernetes.io/cluster/challenge-eks" = "shared"
    "kubernetes.io/role/elb"              = "1"
  }

}

resource "aws_subnet" "public_b_subnet" {
  vpc_id                  = aws_vpc.main_vpc.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "eu-central-1b"
  map_public_ip_on_launch = true

  tags = {
    Name                                  = "Public-Subnet-B"
    "kubernetes.io/cluster/challenge-eks" = "shared"
    "kubernetes.io/role/elb"              = "1"
  }

}

resource "aws_subnet" "private_a_subnet" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "10.0.3.0/24"
  availability_zone = "eu-central-1a"


  tags = {
    Name                                  = "Public-Subnet-A"
    "kubernetes.io/cluster/challenge-eks" = "shared"
    "kubernetes.io/role/internal-elb"     = "1"
  }

}

resource "aws_subnet" "private_b_subnet" {
  vpc_id            = aws_vpc.main_vpc.id
  cidr_block        = "10.0.4.0/24"
  availability_zone = "eu-central-1b"

  tags = {
    Name                                  = "Public-Subnet-A"
    "kubernetes.io/cluster/challenge-eks" = "shared"
    "kubernetes.io/role/internal-elb"     = "1"
  }

}

resource "aws_internet_gateway" "main_iwg" {
  vpc_id = aws_vpc.main_vpc.id

  tags = {
    Name = "Internet-Gateway"
  }

}

resource "aws_route_table" "igw_route_table" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main_iwg.id
  }

  tags = {
    Name = "IGW-Route-Table"
  }
}

resource "aws_route_table_association" "public-1a_assoc" {
  subnet_id      = aws_subnet.public_a_subnet.id
  route_table_id = aws_route_table.igw_route_table.id

}

resource "aws_route_table_association" "public-1b_assoc" {
  subnet_id      = aws_subnet.public_b_subnet.id
  route_table_id = aws_route_table.igw_route_table.id

}

resource "aws_eip" "a_eip" {
  domain = "vpc"
}

resource "aws_eip" "b_eip" {
  domain = "vpc"
}

resource "aws_nat_gateway" "a_ngw" {
  subnet_id     = aws_subnet.public_a_subnet.id # to be connectet to internet gateway
  allocation_id = aws_eip.a_eip.id

  depends_on = [aws_internet_gateway.main_iwg]

  tags = {
    Name = "A-NAT-Gateway"
  }

}

resource "aws_nat_gateway" "b_ngw" {
  subnet_id     = aws_subnet.public_b_subnet.id # to be connectet to internet gateway
  allocation_id = aws_eip.b_eip.id

  depends_on = [aws_internet_gateway.main_iwg]

  tags = {
    Name = "B-NAT-Gateway"
  }

}

resource "aws_route_table" "private_1a_route_table" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.a_ngw.id
  }

  tags = {
    Name = "A-NGW-Route-Table"
  }

}

resource "aws_route_table" "private_1b_route_table" {
  vpc_id = aws_vpc.main_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.b_ngw.id
  }

  tags = {
    Name = "B-NGW-Route-Table"
  }

}

resource "aws_route_table_association" "private_1a_assoc" {
  subnet_id      = aws_subnet.private_a_subnet.id
  route_table_id = aws_route_table.private_1a_route_table.id

}

resource "aws_route_table_association" "private_1b_assoc" {
  subnet_id      = aws_subnet.private_b_subnet.id
  route_table_id = aws_route_table.private_1b_route_table.id

}
