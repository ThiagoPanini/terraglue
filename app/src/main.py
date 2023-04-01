"""An example of Spark application for reading SoR data and creating SoT table.

This scripts uses sparksnake for creating a Spark application to be deployed as
a Glue job on AWS that reads data from SoR layer, transform it and generate a
new SoT table based on Ecommerce public data. The idea is to provide to users
an end to end example on how it's possible to build a Glue job for common
ETL task.

___
"""

# Importing libraries
from sparksnake.manager import SparkETLManager
from sparksnake.utils.log import log_config
from transformers import \
    transform_orders,\
    transform_order_items,\
    transform_customers,\
    transform_payments,\
    transform_reviews,\
    transform_sot

from datetime import datetime


# Setting up a logger object
logger = log_config(logger_name=__file__)

# Defining the list of job arguments
ARGV_LIST = [
    "JOB_NAME",
    "OUTPUT_BUCKET",
    "OUTPUT_DB",
    "OUTPUT_TABLE",
    "CONNECTION_TYPE",
    "UPDATE_BEHAVIOR",
    "PARTITION_NAME",
    "PARTITION_FORMAT",
    "DATA_FORMAT",
    "COMPRESSION",
    "ENABLE_UPDATE_CATALOG",
    "NUM_PARTITIONS"
]

# Defining a dictionary with all data to be read and used on job
DATA_DICT = {
    "tbl_orders": {
        "database": "db_ecommerce",
        "table_name": "tbl_orders",
        "transformation_ctx": "dyf_orders",
        "create_temp_view": True
    },
    "tbl_order_items": {
        "database": "db_ecommerce",
        "table_name": "tbl_order_items",
        "transformation_ctx": "dyf_order_items",
        "create_temp_view": True
    },
    "tbl_customers": {
        "database": "db_ecommerce",
        "table_name": "tbl_customers",
        "transformation_ctx": "dyf_customers",
        "create_temp_view": True
    },
    "tbl_payments": {
        "database": "db_ecommerce",
        "table_name": "tbl_payments",
        "transformation_ctx": "dyf_payments",
        "create_temp_view": True
    },
    "tbl_reviews": {
        "database": "db_ecommerce",
        "table_name": "tbl_reviews",
        "transformation_ctx": "dyf_reviews",
        "create_temp_view": True
    }
}

# Creating a sparksnake object with Glue operation mode
spark_manager = SparkETLManager(
    mode="glue",
    argv_list=ARGV_LIST,
    data_dict=DATA_DICT
)

# Initializing the job
spark_manager.init_job()

# Reading Spark DataFrames from Data Catalog
dfs_dict = spark_manager.generate_dataframes_dict()

# Indexing data do get individual DataFrames
df_orders = dfs_dict["tbl_orders"]
df_order_items = dfs_dict["tbl_order_items"]
df_customers = dfs_dict["tbl_customers"]
df_payments = dfs_dict["tbl_payments"]
df_reviews = dfs_dict["tbl_reviews"]

# Transforming all raw DataFrames
df_orders_prep = transform_orders(df=df_orders)
df_order_items_prep = transform_order_items(df=df_order_items)
df_customers_prep = transform_customers(df=df_customers)
df_payments_prep = transform_payments(
    df=df_payments,
    spark_session=spark_manager.spark
)
df_reviews_prep = transform_reviews(df=df_reviews)

# Joining all DataFrames and preparing the SoT table
df_sot_prep = transform_sot(
    df_orders_prep=df_orders_prep,
    df_order_items_prep=df_order_items_prep,
    df_customers_prep=df_customers_prep,
    df_payments_prep=df_payments_prep,
    df_reviews_prep=df_reviews_prep
)

# Defining a variable for holding the partition value
partition_value = int(datetime.now().strftime(
    spark_manager.args["PARTITION_FORMAT"]))

# Adding a partition column
df_sot_partitioned = spark_manager.add_partition_column(
    partition_name=spark_manager.args["PARTITION_NAME"],
    partition_value=partition_value
)

# Repartitioning the Dataframe to reduce small files and optimize storage
df_sot_repartitioned = spark_manager.repartition_dataframe(
    df=df_sot_partitioned,
    num_partitions=spark_manager.args["NUM_PARTITIONS"]
)

# Defining an URI for output table partition
s3_partition_uri = f"{spark_manager.args['OUTPUT_TABLE_URI']}/"\
    f"{spark_manager.args['PARTITION_NAME']}={partition_value}"

# Dropping partition on s3 (if it exists)
spark_manager.drop_partition(s3_partition_uri=s3_partition_uri)

# Writing data on S3 and cataloging it on Data Catalog
spark_manager.write_and_catalog_data(
    df=df_sot_repartitioned,
    s3_table_uri=spark_manager.args["OUTPUT_TABLE_URI"],
    output_database_name=spark_manager.args["OUTPUT_DB"],
    output_table_name=spark_manager.args["OUTPUT_TABLE"],
    partition_name=spark_manager.args["PARTITION_NAME"],
    connection_type=spark_manager.args["CONNECTION_TYPE"],
    update_behavior=spark_manager.args["UPDATE_BEHAVIOR"],
    compression=spark_manager.args["COMPRESSION"],
    enable_update_catalog=spark_manager.args["ENABLE_UPDATE_CATALOG"],
    output_data_format=spark_manager.args["OUTPUT_DATA_FORMAT"]
)
