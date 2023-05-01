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

from tests.helpers.dataframes import compare_dataframe_schemas
from tests.conftest import spark

from src.transformers import transform_orders,\
    transform_order_items,\
    transform_customers,\
    transform_payments,\
    transform_reviews


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

    assert compare_dataframe_schemas(df_orders_prep, df_prep_expected)


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
    df_order_items
):
    """
    G: given that users want to transform the df_order_items DataFrame
    W: when the function transform_order_items() is called
    T: then the return must be a Spark DataFrame
    """

    assert type(df_order_items) is DataFrame


@pytest.mark.transform_order_items
def test_df_order_items_transformation_generates_the_expected_dataframe_schema(
    expected_dataframes_dict,
    df_order_items_prep
):
    """
    G: given that users want to transform the df_order_items DataFrame
    W: when the function transform_order_items() is called
    T: then the schema of the resulting DataFrame must match the expected
       schema provided by users in the JSON file
    """

    # Unpacking the expected DataFrame object to be tested
    df_prep_expected = expected_dataframes_dict["df_order_items_prep"]

    assert compare_dataframe_schemas(df_order_items_prep, df_prep_expected)


@pytest.mark.transform_order_items
@pytest.mark.exception
def test_exception_on_transforming_df_order_items_dataframe():
    """
    G: given that users want to transform the df_order_items DataFrame
    W: when the function transform_order_items() is called with a wrong arg
    T: then an Exception must be raised
    """

    with pytest.raises(Exception):
        _ = transform_order_items(df=None)


@pytest.mark.transform_customers
def test_df_customers_transformation_generates_a_spark_dataframe_object(
    df_customers
):
    """
    G: given that users want to transform the df_customers DataFrame
    W: when the function transform_customers() is called
    T: then the return must be a Spark DataFrame
    """

    assert type(df_customers) is DataFrame


@pytest.mark.transform_customers
def test_df_customers_transformation_generates_the_expected_dataframe_schema(
    expected_dataframes_dict,
    df_customers_prep
):
    """
    G: given that users want to transform the df_customers DataFrame
    W: when the function transform_customers() is called
    T: then the schema of the resulting DataFrame must match the expected
       schema provided by users in the JSON file
    """

    # Unpacking the expected DataFrame object to be tested
    df_prep_expected = expected_dataframes_dict["df_customers_prep"]

    assert compare_dataframe_schemas(df_customers_prep, df_prep_expected)


@pytest.mark.transform_customers
@pytest.mark.exception
def test_exception_on_transforming_df_customers_dataframe():
    """
    G: given that users want to transform the df_customers DataFrame
    W: when the function transform_customers() is called with a wrong arg
    T: then an Exception must be raised
    """

    with pytest.raises(Exception):
        _ = transform_customers(df=None)


@pytest.mark.transform_payments
def test_df_payments_transformation_generates_a_spark_dataframe_object(
    df_payments
):
    """
    G: given that users want to transform the df_payments DataFrame
    W: when the function transform_payments() is called
    T: then the return must be a Spark DataFrame
    """

    assert type(df_payments) is DataFrame


@pytest.mark.transform_payments
def test_df_payments_transformation_generates_the_expected_dataframe_schema(
    expected_dataframes_dict,
    df_payments_prep
):
    """
    G: given that users want to transform the df_payments DataFrame
    W: when the function transform_payments() is called
    T: then the schema of the resulting DataFrame must match the expected
       schema provided by users in the JSON file
    """

    # Unpacking the expected DataFrame object to be tested
    df_prep_expected = expected_dataframes_dict["df_payments_prep"]

    assert compare_dataframe_schemas(df_payments_prep, df_prep_expected)


@pytest.mark.transform_payments
@pytest.mark.exception
def test_exception_on_transforming_df_payments_dataframe():
    """
    G: given that users want to transform the df_payments DataFrame
    W: when the function transform_payments() is called with a wrong arg
    T: then an Exception must be raised
    """

    with pytest.raises(Exception):
        _ = transform_payments(df=None, spark_session=spark)


@pytest.mark.transform_reviews
def test_df_reviews_transformation_generates_a_spark_dataframe_object(
    df_reviews
):
    """
    G: given that users want to transform the df_reviews DataFrame
    W: when the function transform_reviews() is called
    T: then the return must be a Spark DataFrame
    """

    assert type(df_reviews) is DataFrame


@pytest.mark.transform_reviews
def test_df_reviews_transformation_generates_the_expected_dataframe_schema(
    expected_dataframes_dict,
    df_reviews_prep
):
    """
    G: given that users want to transform the df_reviews DataFrame
    W: when the function transform_reviews() is called
    T: then the schema of the resulting DataFrame must match the expected
       schema provided by users in the JSON file
    """

    # Unpacking the expected DataFrame object to be tested
    df_prep_expected = expected_dataframes_dict["df_reviews_prep"]

    assert compare_dataframe_schemas(df_reviews_prep, df_prep_expected)


@pytest.mark.transform_reviews
@pytest.mark.exception
def test_exception_on_transforming_df_reviews_dataframe():
    """
    G: given that users want to transform the df_reviews DataFrame
    W: when the function transform_reviews() is called with a wrong arg
    T: then an Exception must be raised
    """

    with pytest.raises(Exception):
        _ = transform_reviews(df=None)
