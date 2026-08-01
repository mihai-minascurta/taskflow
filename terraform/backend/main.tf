resource "aws_s3_bucket" "main_bucket" {
  bucket        = "taskflow01082026"
  force_destroy = true

}

resource "aws_s3_bucket_versioning" "main_versioning" {
  bucket = aws_s3_bucket.main_bucket.id

  versioning_configuration {
    status = "Enabled"
  }

}

resource "aws_dynamodb_table" "main_dynamodb" {
  name         = "dynamodbforchallenge"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

}
