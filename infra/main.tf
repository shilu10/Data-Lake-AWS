module tickit_vpc {
    source = "./modules/vpc/"

    vpc_parameters = var.vpc_parameters
    subnet_parameters = var.subnet_parameters 
    igw_parameters = var.igw_parameters 
    rt_parameters = var.rt_parameters
    rt_association_parameters = var.rt_association_parameters
}

resource "aws_security_group" "allow_all" {
  name        = "allow_all"
  description = "Allow All inbound traffic and all outbound traffic"
  vpc_id      = module.tickit_vpc.vpcs["vpc1"].id

  tags = {
    Name = "allow_tls"
  }
}

resource "aws_vpc_security_group_ingress_rule" "allow_all" {
  security_group_id = aws_security_group.allow_all.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = -1 # semantically equivalent to all ports
  ip_protocol       = "all"
  to_port           = -1 # semantically equivalent to all ports
}

resource "aws_vpc_security_group_egress_rule" "allow_all_traffic_ipv4" {
  security_group_id = aws_security_group.allow_all.id
  cidr_ipv4         = "0.0.0.0/0"
  ip_protocol       = "-1" # semantically equivalent to all ports
}

resource "aws_db_subnet_group" "default" {
  name       = "main"
  subnet_ids = [module.tickit_vpc.subnets["subnet1"].id, module.tickit_vpc.subnets["subnet2"].id]

  tags = {
    Name = "My DB subnet group"
  }
}

module "crm"{
    source="./modules/database/"

    allocated_storage = var.crm_allocated_storage
    backup_retention_period = var.crm_backup_retention_period
    engine = var.crm_engine
    engine_version = var.crm_engine_version 
    identifier = var.crm_identifier 
    instance_class = var.crm_instance_class 
    multi_az = var.crm_multi_az 
    username = var.crm_username 
    publicly_accessible = var.crm_publicly_accessible
    password = var.crm_password 
    storage_type = var.crm_storage_type
    storage_encrypted = var.crm_storage_encrypted 
    parameter_group_name = var.crm_parameter_group_name 
    skip_final_snapshot = var.crm_skip_final_snapshot

    db_subnet_group_name = aws_db_subnet_group.default.name
}


module "saas"{
    source="./modules/database/"

    allocated_storage = var.saas_allocated_storage
    backup_retention_period = var.saas_backup_retention_period
    engine = var.saas_engine
    engine_version = var.saas_engine_version 
    identifier = var.saas_identifier 
    instance_class = var.saas_instance_class 
    multi_az = var.saas_multi_az 
    username = var.saas_username 
    password = var.saas_password 
    storage_type = var.saas_storage_type
    publicly_accessible = var.saas_publicly_accessible
    storage_encrypted = var.saas_storage_encrypted 
    parameter_group_name = var.saas_parameter_group_name 
    skip_final_snapshot = var.saas_skip_final_snapshot

    db_subnet_group_name = aws_db_subnet_group.default.name
}
