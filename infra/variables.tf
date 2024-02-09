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

variable "crm_storage_encrypted" {
    type    = bool
}

variable "crm_parameter_group_name" {
    type    = string
}

variable "crm_skip_final_snapshot" {
    type    = bool
}