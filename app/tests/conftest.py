"""Confest file for managing pytest fixtures and other components.

This file will handle essential components and elements to be used on test
scripts along the project, like features and other things.

___
"""

# Importing libraries
import pytest
import findspark

from sparksnake.tester.dataframes import generate_dataframes_dict

from pyspark.sql import SparkSession, DataFrame

from tests.helpers.user_inputs import SOURCE_DATAFRAMES_DICT,\
    EXPECTED_DATAFRAMES_DICT

from src.transformers import transform_orders


# Getting the active SparkSession object (or creating one)
findspark.init()
spark = SparkSession.builder.getOrCreate()


# Returning the SparkSession object as a fixture
@pytest.fixture()
def spark_session(spark: SparkSession = spark) -> SparkSession:
    return spark


# Executing a sparksnake's function to read all predefined DataFrames for test
@pytest.fixture()
def dataframes_dict(spark_session: SparkSession):
    # Creating a empty dictionary to hold all source and expected DataFrames
    dataframes_dict = {}

    # Getting all source DataFrame objects
    dataframes_dict["source"] = generate_dataframes_dict(
        definition_dict=SOURCE_DATAFRAMES_DICT,
        spark_session=spark_session
    )

    # Getting all expected DataFrame objects
    dataframes_dict["expected"] = generate_dataframes_dict(
        definition_dict=EXPECTED_DATAFRAMES_DICT,
        spark_session=spark_session
    )

    return dataframes_dict


# A DataFrame object for the source df_orders DataFrame
@pytest.fixture()
def df_orders(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["source"]["df_orders"]


# A DataFrame object with the expected schema for df_orders
@pytest.fixture()
def df_orders_expected(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["expected"]["df_orders_prep"]


# A DataFrame object that is the result of the df_orders transformation
@pytest.fixture()
def df_orders_prep(df_orders: DataFrame) -> DataFrame:
    return transform_orders(df=df_orders)
