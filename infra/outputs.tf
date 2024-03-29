
####################
## CRM DB
####################

output "crm_db_address" {
    value = module.crm.address
}

output "crm_db_arn" {
    value = module.crm.arn
}

output "crm_db_endpoint" {
    value = module.crm.endpoint
}

output "crm_db_status" {
    value = module.crm.status
}


#####################
## SAAS DB
#####################

output "saas_db_address" {
    value = module.saas.address
}

output "saas_db_arn" {
    value = module.saas.arn
}

output "saas_db_endpoint" {
    value = module.saas.endpoint
}

output "saas_db_status" {
    value = module.saas.status
}


######################
## EC2 
######################

output "ec2_arn" {
	value = aws_instance.this.arn
}

output "ec2_public_dns" {
	value = aws_instance.this.public_dns
}

output "ec2_public_ip" {
	value = aws_instance.this.public_ip
}