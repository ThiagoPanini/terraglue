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

from src.transformers import transform_orders,\
    transform_order_items,\
    transform_customers,\
    transform_payments,\
    transform_reviews,\
    transform_sot


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


""" ------------------------------------------------
       Fixture block for df_orders DataFrame
------------------------------------------------ """


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


""" ------------------------------------------------
      Fixture block for df_order_items DataFrame
------------------------------------------------ """


# A DataFrame object for the source df_order_items DataFrame
@pytest.fixture()
def df_order_items(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["source"]["df_order_items"]


# A DataFrame object with the expected schema for df_order_items
@pytest.fixture()
def df_order_items_expected(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["expected"]["df_order_items_prep"]


# A DataFrame object that is the result of the df_orders transformation
@pytest.fixture()
def df_order_items_prep(df_order_items: DataFrame) -> DataFrame:
    return transform_order_items(df=df_order_items)


""" ------------------------------------------------
      Fixture block for df_customers DataFrame
------------------------------------------------ """


# A DataFrame object for the source df_customers DataFrame
@pytest.fixture()
def df_customers(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["source"]["df_customers"]


# A DataFrame object with the expected schema for df_customers
@pytest.fixture()
def df_customers_expected(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["expected"]["df_customers_prep"]


# A DataFrame object that is the result of the df_customers transformation
@pytest.fixture()
def df_customers_prep(df_customers: DataFrame) -> DataFrame:
    return transform_customers(df=df_customers)


""" ------------------------------------------------
      Fixture block for df_payments DataFrame
------------------------------------------------ """


# A DataFrame object for the source df_payments DataFrame
@pytest.fixture()
def df_payments(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["source"]["df_payments"]


# A DataFrame object with the expected schema for df_payments
@pytest.fixture()
def df_payments_expected(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["expected"]["df_payments_prep"]


# A DataFrame object that is the result of the df_payments transformation
@pytest.fixture()
def df_payments_prep(
    df_payments: DataFrame,
    spark_session: SparkSession
) -> DataFrame:
    return transform_payments(df=df_payments, spark_session=spark_session)


""" ------------------------------------------------
      Fixture block for df_reviews DataFrame
------------------------------------------------ """


# A DataFrame object for the source df_reviews DataFrame
@pytest.fixture()
def df_reviews(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["source"]["df_reviews"]


# A DataFrame object with the expected schema for df_reviews
@pytest.fixture()
def df_reviews_expected(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["expected"]["df_reviews_prep"]


# A DataFrame object that is the result of the df_reviews transformation
@pytest.fixture()
def df_reviews_prep(df_reviews: DataFrame) -> DataFrame:
    return transform_reviews(df=df_reviews)


""" ------------------------------------------------
        Fixture block for df_sot DataFrame
------------------------------------------------ """


# A DataFrame object with the expected schema for df_sot
@pytest.fixture()
def df_sot_expected(dataframes_dict: dict) -> DataFrame:
    return dataframes_dict["expected"]["df_sot_prep"]


# A DataFrame object that is the result of the df_sot transformation
@pytest.fixture()
def df_sot_prep(
    df_orders_prep: DataFrame,
    df_order_items_prep: DataFrame,
    df_customers_prep: DataFrame,
    df_payments_prep: DataFrame,
    df_reviews_prep: DataFrame
) -> DataFrame:
    return transform_sot(
        df_orders_prep=df_orders_prep,
        df_order_items_prep=df_order_items_prep,
        df_customers_prep=df_customers_prep,
        df_payments_prep=df_payments_prep,
        df_reviews_prep=df_reviews_prep
    )
