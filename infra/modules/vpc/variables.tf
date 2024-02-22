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
      use_ng = bool
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

variable "use_nat_gateway" {
  type = bool

  default = false 
}

variable "nat_gateway_params" {
  type = map(object({
    subnet_name = string 
    eip_name = string
  }))

  default = {}
}

variable "eip_params" {
  type = map(object({
    domain = string 
  }))

  default = {}
}