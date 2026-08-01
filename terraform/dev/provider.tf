terraform {
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~>5.0"
    }
  }

  backend "s3" {
    bucket = "taskflow01082026"
    key = "keyforchallengebucket/terraform.tfstate"
    region = "eu-central-1"
    use_lockfile = true
  }

}

provider "aws" {
    region = "eu-central-1"
}