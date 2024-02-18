variable "jdbc_connection_url" {
    type = string 
}

variable "connection_username" {
    type = string 
}

variable "connection_password" {
    type = string 
}

variable "availability_zone" {
    type = string 
}

variable "subnet_id" {
    type = string 
}

variable "security_group_id_list" {
    type = list 
}

variable "glue_catalog_database_name" {
    type = string 
}

variable "glue_connection_name" {
    type = string 
}

variable "glue_crawler_name" {
    type = string 
}

variable "iam_role_arn" {
    type = string 
}

variable "database_name" {
    type = string 
}

#variable "job_name" {
 #   type = string 
#}

#variable "job_iam_tole_arn" {
 #   type = string 
#}

#variable "script_s3_location" {
 #   type = string 
#}