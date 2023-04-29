"""Confest file for managing pytest fixtures and other components.

This file will handle essential components and elements to be used on test
scripts along the project, like features and other things.

___
"""

# Importing libraries
import pytest
import os
import findspark

from pyspark.sql import SparkSession, DataFrame

from tests.helpers.dataframes import create_spark_dataframe_from_json_info

from src.transformers import transform_orders


# Creating a SparkSession object
findspark.init()
spark = SparkSession.builder.getOrCreate()

# Defining paths for JSON files with infos to create Spark DataFrames
SOURCE_JSON_SCHEMAS_PATH = os.path.join(
    os.getcwd(), "app/tests/configs/source_schemas.json"
)


# A dictionary with all source DataFrames to be used on the Glue job
@pytest.fixture()
def source_dataframes_dict() -> dict:
    return create_spark_dataframe_from_json_info(
        json_path=SOURCE_JSON_SCHEMAS_PATH,
        spark=spark
    )


# A DataFrame object extracted from JSON for test purposes only
@pytest.fixture()
def df_test_null_data(source_dataframes_dict: dict) -> DataFrame:
    return source_dataframes_dict["df_test_null_data"]


# A df_orders sample DataFrame
@pytest.fixture()
def df_orders(source_dataframes_dict: dict) -> DataFrame:
    return source_dataframes_dict["df_orders"]


# A df_orders_prep generated running the transform_orders function
@pytest.fixture()
def df_orders_prep(df_orders) -> DataFrame:
    return transform_orders(df=df_orders)
