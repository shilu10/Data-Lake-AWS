
variable "security_group_name" {
	type = string
}

variable "security_group_description" {
	type = string
}

variable "vpc_id" {
	type = string
}

variable "tags" {
	type = map(string)
}

variable "sg_ingress_parameters" {
	type = map(object({
       cidr_ipv4 = string
       from_port     = number
       to_port = number
       ip_protocol = string
    }))
}

variable "sg_egress_parameters" {
	type = map(object({
       cidr_ipv4 = string

       ip_protocol = string
    }))
}