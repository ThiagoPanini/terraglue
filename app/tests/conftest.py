"""Confest file for managing pytest fixtures and other components.

This file will handle essential components and elements to be used on test
scripts along the project, like features and other things.

___
"""

# Importing libraries
import pytest

from pyspark.sql import SparkSession, DataFrame

from samples.dataframes import generate_samples_dataframes
from samples.data import SAMPLES_DICT


# Creating a SparkSession object
spark = SparkSession.builder.getOrCreate()


# A  dictionary with DataFrames samples to be used on tests
@pytest.fixture()
def samples_dfs_dict() -> dict:
    return generate_samples_dataframes(
        spark=spark,
        samples_dict=SAMPLES_DICT
    )


# A tbl_brecommerce_orders sample DataFrame
@pytest.fixture()
def df_orders(samples_dfs_dict: dict) -> DataFrame:
    return samples_dfs_dict["tbl_brecommerce_orders"]
