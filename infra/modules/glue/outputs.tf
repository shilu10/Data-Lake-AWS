output "crawler_id" {
    value = aws_glue_crawler.this.id 
}

output "catalog_database_id" {
    value = aws_glue_catalog_database.this.id 
}

output "glue_connection_id" {
    value = aws_glue_connection.this.id 
}

#output "glue_job_id" {
 #   value = aws_glue_job.this.id 
#}