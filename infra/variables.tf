
#####################
# CRM DB
######################

variable "crm_allocated_storage" {
    type    = number
}

variable "crm_backup_retention_period" {
    type    = number
}

variable "crm_engine" {
    type    = string
}

variable "crm_engine_version" {
    type    = string
}

variable "crm_identifier" {
    type    = string
}

variable "crm_instance_class" {
    type    = string
}

variable "crm_multi_az" {
    type    = bool
}

variable "crm_username" {
    type    = string
}

variable "crm_password" {
    type    = string
}

variable "crm_storage_type" {
    type = string
}

variable "crm_storage_encrypted" {
    type    = bool
}

variable "crm_parameter_group_name" {
    type    = string
}

variable "crm_skip_final_snapshot" {
    type    = bool
}

variable "crm_publicly_accessible" {
    type = bool
}



#########################
## SAAS DB
#########################

variable "saas_allocated_storage" {
    type    = number
}

variable "saas_backup_retention_period" {
    type    = number
}

variable "saas_engine" {
    type    = string
}

variable "saas_engine_version" {
    type    = string
}

variable "saas_identifier" {
    type    = string
}

variable "saas_instance_class" {
    type    = string
}

variable "saas_multi_az" {
    type    = bool
}

variable "saas_username" {
    type    = string
}

variable "saas_password" {
    type    = string
}

variable "saas_storage_type" {
    type = string 
}

variable "saas_storage_encrypted" {
    type    = bool
}

variable "saas_parameter_group_name" {
    type    = string
}

variable "saas_skip_final_snapshot" {
    type    = bool
}

variable "saas_publicly_accessible" {
    type = bool
}



#######################
## EC2
#######################

variable "ec2_instance_type"{
  type = string 
}

variable "ec2_associate_public_ip_address"{
  type = bool 
}

variable "ec2_key_name" {
    type = string 
}

variable "ec2_key_filename" {
    type = string 
}

variable "ec2_tags" {
  type = map(string)
}



####################
# Security Groups
####################

variable "db_security_group_name"{
  type = string
}

variable "db_security_group_description"{
  type = string
}

variable "db_sg_ingress_parameters"{
  type = map(object({
       cidr_ipv4 = string
       from_port     = number
       to_port = number
       ip_protocol = string
    }))
}

variable "db_sg_egress_parameters"{
  type = map(object({
       cidr_ipv4 = string

       ip_protocol = string
    }))
}

variable "db_sg_tags" {
  type = map(string)
}

# ec2
variable "ec2_security_group_name"{
  type = string
}

variable "ec2_security_group_description"{
  type = string
}

variable "ec2_sg_ingress_parameters"{
  type = map(object({
       cidr_ipv4 = string
       from_port     = number
       to_port = number
       ip_protocol = string
    }))
}

variable "ec2_sg_egress_parameters"{
  type = map(object({
       cidr_ipv4 = string

       ip_protocol = string
    }))
}

variable "ec2_sg_tags" {
  type = map(string)
}



########################
## VPC
########################

variable "vpc_parameters" {
  description = "VPC parameters"
  type = map(object({
    cidr_block           = string
    enable_dns_support   = bool
    enable_dns_hostnames = bool
    tags                 = map(string)
  }))
  default = {}
}


variable "subnet_parameters" {
  description = "Subnet parameters"
  type = map(object({
    cidr_block = string
    vpc_name   = string
    availability_zone = string 
    map_public_ip_on_launch = bool
    tags       = map(string)
  }))
  default = {}
}

variable "igw_parameters" {
  description = "IGW parameters"
  type = map(object({
    vpc_name = string
    tags     = map(string)
  }))
  default = {}
}


variable "rt_parameters" {
  description = "RT parameters"
  type = map(object({
    vpc_name = string
    tags     = map(string)
    routes = list(object({
      cidr_block = string
      use_igw    = bool
      gateway_id = string
    }))
  }))
  default = {}
}
variable "rt_association_parameters" {
  description = "RT association parameters"
  type = map(object({
    subnet_name = string
    rt_name     = string
  }))
  default = {}
}

# CRM glue
variable "crm_glue_catalog_database_name" {
  type = string 
}

variable "crm_glue_connection_name" {
  type = string 
}

variable "crm_glue_crawler_name" {
  type = string 
}

variable "crm_database_name" {
  type = string 
}