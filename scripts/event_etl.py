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
        "dbtable": "tickit.event",
        "connectionName": "tickit_connection",
    },
    transformation_ctx="MySQL_node1708609890536",
)

# Script generated for node Change Schema
ChangeSchema_node1708611296948 = ApplyMapping.apply(
    frame=MySQL_node1708609890536,
    mappings=[
        ("event_id", "int", "event_id", "int"),
        ("venue_id", "int", "venue_id", "int"),
        ("cat_id", "int", "category_id", "int"),
        ("date_id", "int", "date_id", "int"),
        ("event_name", "string", "event_name", "string"),
        ("start_time", "timestamp", "start_time", "timestamp"),
    ],
    transformation_ctx="ChangeSchema_node1708611296948",
)

job.commit()
