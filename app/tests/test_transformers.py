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

from sparksnake.tester.dataframes import compare_schemas


@pytest.mark.transform_orders
def test_df_orders_transformation_generates_a_spark_dataframe_object(
    df_orders_prep
):
    """
    G: Given that users want to transform the df_orders DataFrame
    W: When the function transform_orders() is called
    T: Then the return must be a Spark DataFrame
    """

    assert type(df_orders_prep) is DataFrame


@pytest.mark.transform_orders
def test_df_orders_transformation_generates_the_expected_schema(
    df_orders_prep,
    df_orders_expected
):
    """
    G: Given that users want to transform the df_orders DataFrame
    W: When the function transform_orders() is called
    T: Then the schema of the returned DataFrame must match the expected
    """

    assert compare_schemas(df1=df_orders_prep, df2=df_orders_expected,
                           compare_nullable_info=False)
