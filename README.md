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

### Steps to create table and populate data into database tables
- Login to the Database EC2 instance:
    $ chmod 400 private_key.pem 
    $ ssh -i private_key.pem ubuntu@public_ec2_ip 
    $ sudo su - 
    $ apt update -y 
    $ apt install python3-pip --quiet 
    $ export ACCESS_TOKEN="your_access_token" 
    $ export SECRET_ACCESS_TOKEN="your_secret_access_token"
    $ git clone https://github.com/shilu10/Data-Lake-AWS.git
    $ cd Data-Lake-AWS/
    $ pip3 install -r requirements.txt
    $ cd db_py_files/
    $ python3 create_tables.py --host=0.0.0.0 --username='admin' --password='secret' --port=3306 --rdbms-type='mysql' --database-name='tickit' --tables-to-include=['category', 'venue']
    $ python3 --insert_data.py --host=0.0.0.0 --username='admin' --password='secret' --rdbms-type='mysql' --database-name='tickit' --tables-to-include=['category', 'venue']