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