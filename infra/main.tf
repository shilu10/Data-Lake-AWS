
module 'crm'{
    path='../modules/database/'

    allocated_storage = var.crm_allocated_storage
    backup_retention_period = var.crm_backup_retention_period
    engine = var.crm_engine
    engine_version = var.crm_engine_version 
    identifier = var.crm_identifier 
    instance_class = var.crm_instance_class 
    multi_az = var.crm_multi_az 
    username = var.crm_username 
    password = var.crm_password 
    storage_encrypted = var.crm_storage_encrypted 
    parameter_group_name = var.crm_parameter_group_name 
    skip_final_snapshot = var.crm_skip_final_snapshot
}