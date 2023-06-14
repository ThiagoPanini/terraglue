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

from src.transformers import transform_orders,\
    transform_order_items,\
    transform_customers,\
    transform_payments,\
    transform_reviews,\
    transform_sot


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

    assert compare_schemas(
        df1=df_orders_prep,
        df2=df_orders_expected,
        compare_nullable_info=False
    )


@pytest.mark.transform_orders
def test_error_on_calling_transform_orders_function():
    """
    G: Given that users want to transform the df_orders DataFrame
    W: When the function transform_orders() is called with an invalid
       argument (i.e. an object different than a Spark DataFrame)
    T: Then an Exception must be raised
    """
    with pytest.raises(Exception):
        _ = transform_orders(df=None)


@pytest.mark.transform_order_items
def test_df_order_items_transformation_generates_a_spark_dataframe_object(
    df_order_items_prep
):
    """
    G: Given that users want to transform the df_order_items DataFrame
    W: When the function transform_order_items() is called
    T: Then the return must be a Spark DataFrame
    """

    assert type(df_order_items_prep) is DataFrame


@pytest.mark.transform_order_items
def test_df_order_items_transformation_generates_the_expected_schema(
    df_order_items_prep,
    df_order_items_expected
):
    """
    G: Given that users want to transform the df_order_items DataFrame
    W: When the function transform_order_items() is called
    T: Then the schema of the returned DataFrame must match the expected
    """

    assert compare_schemas(
        df1=df_order_items_prep,
        df2=df_order_items_expected,
        compare_nullable_info=False
    )


@pytest.mark.transform_order_items
def test_error_on_calling_transform_order_items_function():
    """
    G: Given that users want to transform the df_order_items DataFrame
    W: When the function transform_order_items() is called with an invalid
       argument (i.e. an object different than a Spark DataFrame)
    T: Then an Exception must be raised
    """
    with pytest.raises(Exception):
        _ = transform_order_items(df=None)


@pytest.mark.transform_customers
def test_df_customers_transformation_generates_a_spark_dataframe_object(
    df_customers_prep
):
    """
    G: Given that users want to transform the df_customers DataFrame
    W: When the function transform_customers() is called
    T: Then the return must be a Spark DataFrame
    """

    assert type(df_customers_prep) is DataFrame


@pytest.mark.transform_customers
def test_df_customers_transformation_generates_the_expected_schema(
    df_customers_prep,
    df_customers_expected
):
    """
    G: Given that users want to transform the df_customers DataFrame
    W: When the function transform_customers() is called
    T: Then the schema of the returned DataFrame must match the expected
    """

    assert compare_schemas(
        df1=df_customers_prep,
        df2=df_customers_expected,
        compare_nullable_info=False
    )


@pytest.mark.transform_customers
def test_error_on_calling_transform_customers_function():
    """
    G: Given that users want to transform the df_customers DataFrame
    W: When the function transform_customers() is called with an invalid
       argument (i.e. an object different than a Spark DataFrame)
    T: Then an Exception must be raised
    """
    with pytest.raises(Exception):
        _ = transform_customers(df=None)


@pytest.mark.transform_payments
def test_df_payments_transformation_generates_a_spark_dataframe_object(
    df_payments_prep
):
    """
    G: Given that users want to transform the df_payments DataFrame
    W: When the function transform_payments() is called
    T: Then the return must be a Spark DataFrame
    """

    assert type(df_payments_prep) is DataFrame


@pytest.mark.transform_payments
def test_df_payments_transformation_generates_the_expected_schema(
    df_payments_prep,
    df_payments_expected
):
    """
    G: Given that users want to transform the df_payments DataFrame
    W: When the function transform_payments() is called
    T: Then the schema of the returned DataFrame must match the expected
    """

    assert compare_schemas(
        df1=df_payments_prep,
        df2=df_payments_expected,
        compare_nullable_info=False
    )


@pytest.mark.transform_payments
def test_error_on_calling_transform_payments_function():
    """
    G: Given that users want to transform the df_payments DataFrame
    W: When the function transform_payments() is called with an invalid
       argument (i.e. an object different than a Spark DataFrame)
    T: Then an Exception must be raised
    """
    with pytest.raises(Exception):
        _ = transform_payments(df=None, spark_session=None)


@pytest.mark.transform_reviews
def test_df_reviews_transformation_generates_a_spark_dataframe_object(
    df_reviews_prep
):
    """
    G: Given that users want to transform the df_reviews DataFrame
    W: When the function transform_reviews() is called
    T: Then the return must be a Spark DataFrame
    """

    assert type(df_reviews_prep) is DataFrame


@pytest.mark.transform_reviews
def test_df_reviews_transformation_generates_the_expected_schema(
    df_reviews_prep,
    df_reviews_expected
):
    """
    G: Given that users want to transform the df_reviews DataFrame
    W: When the function transform_reviews() is called
    T: Then the schema of the returned DataFrame must match the expected
    """

    assert compare_schemas(
        df1=df_reviews_prep,
        df2=df_reviews_expected,
        compare_nullable_info=False
    )


@pytest.mark.transform_reviews
def test_error_on_calling_transform_reviews_function():
    """
    G: Given that users want to transform the df_reviews DataFrame
    W: When the function transform_reviews() is called with an invalid
       argument (i.e. an object different than a Spark DataFrame)
    T: Then an Exception must be raised
    """
    with pytest.raises(Exception):
        _ = transform_reviews(df=None)


@pytest.mark.transform_sot
def test_df_sot_transformation_generates_a_spark_dataframe_object(
    df_sot_prep
):
    """
    G: Given that users want to transform the df_sot DataFrame
    W: When the function transform_sot() is called
    T: Then the return must be a Spark DataFrame
    """

    assert type(df_sot_prep) is DataFrame


@pytest.mark.transform_sot
def test_df_sot_transformation_generates_the_expected_schema(
    df_sot_prep,
    df_sot_expected
):
    """
    G: Given that users want to transform the df_sot DataFrame
    W: When the function transform_sot() is called
    T: Then the schema of the returned DataFrame must match the expected
    """

    assert compare_schemas(
        df1=df_sot_prep,
        df2=df_sot_expected,
        compare_nullable_info=False
    )


@pytest.mark.transform_sot
def test_error_on_calling_transform_sot_function():
    """
    G: Given that users want to transform the df_sot DataFrame
    W: When the function transform_sot() is called with an invalid
       argument (i.e. an object different than a Spark DataFrame)
    T: Then an Exception must be raised
    """
    with pytest.raises(Exception):
        _ = transform_sot(
            df_orders_prep=None,
            df_order_items_prep=None,
            df_customers_prep=None,
            df_payments_prep=None,
            df_reviews_prep=None
        )
