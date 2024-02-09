
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
    storage_encrypted = var.crm_storage_encrypted 
    parameter_group_name = var.crm_parameter_group_name 
    skip_final_snapshot = var.crm_skip_final_snapshot
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
    publicly_accessible = var.saas_publicly_accessible
    storage_encrypted = var.saas_storage_encrypted 
    parameter_group_name = var.saas_parameter_group_name 
    skip_final_snapshot = var.saas_skip_final_snapshot
}