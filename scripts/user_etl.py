import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node MySQL
MySQL_node1708609890536 = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "tickit.user",
        "connectionName": "tickit_connection",
    },
    transformation_ctx="MySQL_node1708609890536",
)

# Script generated for node Change Schema
ChangeSchema_node1708611296948 = ApplyMapping.apply(
    frame=MySQL_node1708609890536,
    mappings=[
        ("user_id", "int", "user_id", "int"),
        ("first_name", "string", "first_name", "string"),
        ("last_name", "string", "last_name", "string"),
        ("city", "string", "city", "string"),
        ("state", "string", "state", "string"),
        ("like_sports", "boolean", "like_sports", "boolean"),
        ("like_theatre", "boolean", "like_theatre", "boolean"),
        ("like_concerts", "boolean", "like_concerts", "boolean"),
        ("like_jazz", "boolean", "like_jazz", "boolean"),
        ("like_classical", "boolean", "like_classical", "boolean"),
        ("like_opera", "boolean", "like_opera", "boolean"),
        ("like_rock", "boolean", "like_rock", "boolean"),
        ("like_vegas", "boolean", "like_vegas", "boolean"),
        ("like_broadway", "boolean", "like_broadway", "boolean"),
        ("like_musicals", "boolean", "like_musicals", "boolean"),
    ],
    transformation_ctx="ChangeSchema_node1708611296948",
)

job.commit()
