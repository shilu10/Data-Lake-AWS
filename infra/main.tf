#####################################
# VPC 
#####################################
module "tickit_vpc" {
    source = "./modules/vpc/"

    use_nat_gateway = var.use_nat_gateway
    nat_gateway_params = var.nat_gateway_params 
    eip_params = var.eip_params
    vpc_parameters = var.vpc_parameters
    subnet_parameters = var.subnet_parameters 
    igw_parameters = var.igw_parameters 
    rt_parameters = var.rt_parameters
    rt_association_parameters = var.rt_association_parameters
}


########################################
# Security Groups
########################################
module "db_security_group" {
  source = "./modules/security_group"

  security_group_name = var.db_security_group_name
  security_group_description = var.db_security_group_description
  vpc_id = module.tickit_vpc.vpcs["vpc_tickit"].id
  sg_ingress_parameters = var.db_sg_ingress_parameters
  sg_egress_parameters = var.db_sg_egress_parameters

  tags = var.db_sg_tags
}

module "ec2_security_group" {
  source = "./modules/security_group"

  security_group_name = var.ec2_security_group_name
  security_group_description = var.ec2_security_group_description
  vpc_id = module.tickit_vpc.vpcs["vpc_tickit"].id
  sg_ingress_parameters = var.ec2_sg_ingress_parameters
  sg_egress_parameters = var.ec2_sg_egress_parameters

  tags = var.ec2_sg_tags
}

resource "aws_security_group" "self_referencing" {
  name        = "self-referencing-sg"
  description = "Allow ingress from the same security group"
  vpc_id      = module.tickit_vpc.vpcs["vpc_tickit"].id

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    self = true
  }

  tags = {
    Name = "self-referencing-sg"
  }
}

module "glue_security_group" {
  source = "./modules/security_group"

  security_group_name = var.glue_security_group_name
  security_group_description = var.glue_security_group_description
  vpc_id = module.tickit_vpc.vpcs["vpc_tickit"].id
  sg_ingress_parameters = var.glue_sg_ingress_parameters
  sg_egress_parameters = var.glue_sg_egress_parameters

  tags = var.db_sg_tags
}

#####################################
# AMI 
#####################################
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

######################################
# Key Pair 
######################################
resource "aws_key_pair" "this" {
key_name = var.ec2_key_name
public_key = tls_private_key.this.public_key_openssh
}

resource "tls_private_key" "this" {
algorithm = "RSA"
rsa_bits  = 4096
}

resource "local_file" "this" {
content  = tls_private_key.this.private_key_pem
filename = var.ec2_key_filename
}

#######################################
# Ec2 instance 
#######################################
resource "aws_instance" "this" {
  ami = data.aws_ami.ubuntu.id
  subnet_id = module.tickit_vpc.subnets["public_subnet_1"].id

  associate_public_ip_address = var.ec2_associate_public_ip_address
  instance_type = var.ec2_instance_type 

  key_name = aws_key_pair.this.key_name
  security_groups = [module.ec2_security_group.id]

  tags = var.ec2_tags

  user_data = <<-EOF
              #!/bin/bash
              apt install python3-pip 
              apt install mysql-server
              pip3 install mysql-connector 
              pip3 install pandas sqlalchemy psycopg2-binary
              # Add additional commands or configurations here
            EOF

}

########################################
# Database Subnet Group 
########################################
resource "aws_db_subnet_group" "this" {
  name       = "crm"
  subnet_ids = [module.tickit_vpc.subnets["private_subnet_1"].id, module.tickit_vpc.subnets["private_subnet_2"].id]

  tags = {
    Name = "CRM Subnet Group"
  }
}


########################################
# Databases 
########################################
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

    db_subnet_group_name = aws_db_subnet_group.this.name
    vpc_security_group_ids = [module.db_security_group.id, aws_security_group.self_referencing.id]
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

    db_subnet_group_name = aws_db_subnet_group.this.name
    vpc_security_group_ids = [module.db_security_group.id, aws_security_group.self_referencing.id]
}


#######################
# IAM for GLUE 
########################
resource "aws_iam_role" "this" {
  name = "crawler_role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "this" {
  name   = "crawler_policy"
  role   = aws_iam_role.this.name

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "*"
        ],
        Resource = "*"
      }
    ]
  })
}


locals {
  subnet_id_1 = module.tickit_vpc.subnets["private_subnet_1"].id
}

locals {
  subnet_id_2 = module.tickit_vpc.subnets["private_subnet_2"].id
}

############################
## GLUE 
############################

module "crm_glue" {
  source = "./modules/glue/"

  jdbc_connection_url = "jdbc:mysql://${module.crm.endpoint}"
  connection_username = var.crm_username
  connection_password = var.crm_password 
  availability_zone = module.crm.availability_zone
  subnet_id = module.crm.availability_zone == "us-east-1a" ? local.subnet_id_1 : local.subnet_id_2
  security_group_id_list = [aws_security_group.self_referencing.id, module.glue_security_group.id]
   
  glue_catalog_database_name = var.crm_glue_catalog_database_name 

  glue_connection_name = var.crm_glue_connection_name
  glue_crawler_name = var.crm_glue_crawler_name 
  iam_role_arn = aws_iam_role.this.arn 
  database_name = var.crm_database_name 

}