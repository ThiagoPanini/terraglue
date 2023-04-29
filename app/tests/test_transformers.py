"""Test cases for DAG transformation functions in transformer.py module

This file handles all unit tests to check if the transformations coded on
transformers.py src module are working properly. The idea is to ensure that
transformations are generating the expected result based on the output
DataFrame schemas.

___
"""

# Importing libraries
import pytest

from pyspark.sql import DataFrame


@pytest.mark.transformers
@pytest.mark.transform_orders
def test_df_orders_transformation_generates_a_spark_dataframe_object(
    df_orders_prep
):
    """
    G: given that users want to transform the df_orders DataFrame
    W: when the function transform_orders() is called
    T: then the return must be a Spark DataFrame
    """

    assert type(df_orders_prep) is DataFrame
