resource "aws_glue_connection" "this" {
  connection_properties = {
    JDBC_CONNECTION_URL = var.jdbc_connection_url
    PASSWORD            = var.connection_password
    USERNAME            = var.connection_username
  }

  name = var.glue_connection_name

  physical_connection_requirements {
  #  availability_zone      = var.availability_zone
    security_group_id_list = var.security_group_id_list
    subnet_id              = var.subnet_id
  }
}

resource "aws_glue_catalog_database" "this" {
  name = var.glue_catalog_database_name
}

resource "aws_glue_crawler" "this" {
  database_name = aws_glue_catalog_database.this.name
  name          = var.glue_crawler_name
  role          = var.iam_role_arn

  jdbc_target {
    connection_name = aws_glue_connection.this.name
    path            = var.database_name
  }
}