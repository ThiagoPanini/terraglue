import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1665022771724 = glueContext.create_dynamic_frame.from_catalog(
    database="ra8",
    table_name="orders",
    transformation_ctx="AWSGlueDataCatalog_node1665022771724",
)

# Script generated for node AWS Glue Data Catalog
AWSGlueDataCatalog_node1665022811044 = glueContext.create_dynamic_frame.from_catalog(
    database="ra8",
    table_name="customers",
    transformation_ctx="AWSGlueDataCatalog_node1665022811044",
)

# Script generated for node Renamed keys for Join
RenamedkeysforJoin_node1665022866494 = ApplyMapping.apply(
    frame=AWSGlueDataCatalog_node1665022811044,
    mappings=[
        ("customer_city", "string", "customer_city", "string"),
        ("customer_id", "string", "right_customer_id", "string"),
        ("customer_state", "string", "customer_state", "string"),
        ("customer_unique_id", "string", "customer_unique_id", "string"),
        ("customer_zip_code_prefix", "string", "customer_zip_code_prefix", "string"),
    ],
    transformation_ctx="RenamedkeysforJoin_node1665022866494",
)

# Script generated for node Join
AWSGlueDataCatalog_node1665022771724DF = AWSGlueDataCatalog_node1665022771724.toDF()
RenamedkeysforJoin_node1665022866494DF = RenamedkeysforJoin_node1665022866494.toDF()
Join_node1665022798405 = DynamicFrame.fromDF(
    AWSGlueDataCatalog_node1665022771724DF.join(
        RenamedkeysforJoin_node1665022866494DF,
        (
            AWSGlueDataCatalog_node1665022771724DF["customer_id"]
            == RenamedkeysforJoin_node1665022866494DF["right_customer_id"]
        ),
        "left",
    ),
    glueContext,
    "Join_node1665022798405",
)

# Script generated for node Apply Mapping
ApplyMapping_node1665022909431 = ApplyMapping.apply(
    frame=Join_node1665022798405,
    mappings=[
        ("customer_id", "string", "customer_id", "string"),
        ("order_approved_at", "string", "order_approved_at", "string"),
        (
            "order_delivered_carrier_date",
            "string",
            "order_delivered_carrier_date",
            "string",
        ),
        (
            "order_delivered_customer_date",
            "string",
            "order_delivered_customer_date",
            "string",
        ),
        (
            "order_estimated_delivery_date",
            "string",
            "order_estimated_delivery_date",
            "string",
        ),
        ("order_id", "string", "order_id", "string"),
        ("order_purchase_timestamp", "string", "order_purchase_timestamp", "string"),
        ("order_status", "string", "order_status", "string"),
        ("customer_city", "string", "customer_city", "string"),
        ("customer_state", "string", "customer_state", "string"),
        ("customer_unique_id", "string", "customer_unique_id", "string"),
        ("customer_zip_code_prefix", "string", "customer_zip_code_prefix", "string"),
    ],
    transformation_ctx="ApplyMapping_node1665022909431",
)

# Script generated for node Amazon S3
AmazonS3_node1665022935080 = glueContext.getSink(
    path="s3://sbx-sot-data-059028725593-us-east-1",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1665022935080",
)
AmazonS3_node1665022935080.setCatalogInfo(
    catalogDatabase="ra8", catalogTableName="tbl_sot_products_costumers"
)
AmazonS3_node1665022935080.setFormat("glueparquet")
AmazonS3_node1665022935080.writeFrame(ApplyMapping_node1665022909431)
job.commit()
