# Data-Lake-AWS

#### Conceptual Data Model:
![alt text](conceptual_data_model.png)

#### Logical Data Model:
![alt text](logical_data_model.png)


Download the tickit.zip from data directory

### create s3 bucket command
aws s3api create-bucket --bucket=<bucket-name> --region=us-east-1


### Move the data to created s3 bucket
aws s3 cp Downloads/tickitdb/ s3://tickit-data-1/ --recursive 


### Create S3 for terraform backend
aws s3api create-bucket --bucket=tickit-backend --region=us-east-1