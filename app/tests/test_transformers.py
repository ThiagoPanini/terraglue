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

from src.transformers import transform_orders


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


@pytest.mark.transform_orders
def test_df_orders_transformation_generates_the_expected_dataframe_schema(
    expected_dataframes_dict,
    df_orders_prep
):
    """
    G: given that users want to transform the df_orders DataFrame
    W: when the function transform_orders() is called
    T: then the schema of the resulting DataFrame must match the expected
       schema provided by users in the JSON file
    """

    # Unpacking the expected DataFrame object to be tested
    df_prep_expected = expected_dataframes_dict["df_orders_prep"]

    assert df_prep_expected.schema == df_orders_prep.schema


@pytest.mark.transform_orders
@pytest.mark.exception
def test_exception_on_transforming_df_orders_dataframe():
    """
    G: given that users want to transform the df_orders DataFrame
    W: when the function transform_orders() is called with a wrong argument
    T: then an Exception must be raised
    """

    with pytest.raises(Exception):
        _ = transform_orders(df=None)


@pytest.mark.transform_order_items
def test_df_order_items_transformation_generates_a_spark_dataframe_object(
    df_orders_prep
):
    """
    G: given that users want to transform the df_orders DataFrame
    W: when the function transform_orders() is called
    T: then the return must be a Spark DataFrame
    """

    assert type(df_orders_prep) is DataFrame
