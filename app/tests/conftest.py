"""Confest file for managing pytest fixtures and other components.

This file will handle essential components and elements to be used on test
scripts along the project, like features and other things.

___
"""

# Importing libraries
import pytest
import os

from pyspark.sql import SparkSession, DataFrame

from tests.helpers.dataframes import create_spark_dataframe_from_json_info,\
    get_json_data_info

# from src.transformers import transform_orders


# Initializing findspark in case of using a Windows platform
if os.name == "nt":
    import findspark
    findspark.init()

# Creating a SparkSession object
spark = SparkSession.builder.getOrCreate()

# Defining paths for JSON files with infos to create Spark DataFrames
SOURCE_JSON_SCHEMAS_PATH = os.path.join(
    os.getcwd(), "app/tests/configs/source_schemas.json"
)


# A JSON file loaded with source schema definition
@pytest.fixture()
def json_data_info_source() -> dict:
    return get_json_data_info(
        json_path=SOURCE_JSON_SCHEMAS_PATH,
        json_main_key="source"
    )


# A dictionary with all source DataFrames to be used on the Glue job
@pytest.fixture()
def source_dataframes_dict() -> dict:
    return create_spark_dataframe_from_json_info(
        json_path=SOURCE_JSON_SCHEMAS_PATH,
        spark=spark
    )


# A df_orders sample DataFrame
@pytest.fixture()
def df_orders(source_dataframes_dict: dict) -> DataFrame:
    return source_dataframes_dict["df_orders"]


# A df_orders_prep generated running the transform_orders function
"""
@pytest.fixture()
def df_orders_prep(df_orders) -> DataFrame:
    return transform_orders(df=df_orders)
"""
