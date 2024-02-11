variable "allocated_storage" {
    type    = number
}

variable "backup_retention_period" {
    type    = number
}

variable "engine" {
    type    = string
}

variable "engine_version" {
    type    = string
}

variable "identifier" {
    type    = string
}

variable "instance_class" {
    type    = string
}

variable "multi_az" {
    type    = bool
}

variable "username" {
    type    = string
}

variable "password" {
    type    = string
}

variable "storage_encrypted" {
    type    = bool
}

variable "parameter_group_name" {
    type    = string
}

variable "skip_final_snapshot" {
    type    = bool
}

variable "publicly_accessible" {
    type = bool
}

variable "storage_type" {
    type = string 
}

variable "db_subnet_group_name" {
    type = string 
}