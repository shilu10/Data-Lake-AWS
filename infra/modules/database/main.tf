
resource "aws_db_instance" "this" {
  allocated_storage           = var.allocated_storage
  backup_retention_period     = var.backup_retention_period
  engine                      = var.engine
  engine_version              = var.engine_version
  identifier                  = var.identifier
  instance_class              = var.instance_class
  multi_az                    = var.multi_az # Custom for Oracle does not support multi-az
  password                    = var.password
  username                    = var.username
  db_subnet_group_name = var.db_subnet_group_name
  vpc_security_group_ids = var.vpc_security_group_ids

  storage_type = var.storage_type
  publicly_accessible = var.publicly_accessible
  storage_encrypted           = var.storage_encrypted
  parameter_group_name = var.parameter_group_name
  skip_final_snapshot  = var.skip_final_snapshot


  timeouts {
    create = "3h"
    delete = "3h"
    update = "3h"
  }
}