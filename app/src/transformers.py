"""Centralizes transformation functions to be applied on the main application.

This module holds functions that builds DAGs for transforming Spark DataFrames
in a Spark application execution. The big idea is to organize the entire
application in order to have business rules applied in one module. With this
approach, this module can be imported in a main script (e.g. main.py) and
its functions can be called to map the DAGs to raw DataFrames to get
transformations applied.

___
"""

# Importing libraries
from sparksnake.utils.log import log_config
from sparksnake.manager import SparkETLManager

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, sum, mean, max, min, count, round


# Setting up a logger object
logger = log_config(logger_name=__file__)


# Transformation method: df_orders
def transform_orders(df: DataFrame) -> DataFrame:
    """Creates a DAG to transform orders data.

    This function is responsible for applying the business rules to the
    orders DataFrame in order to create a new and prepared DataFrame object.
    Here are the steps taken:

    1. Cast date attributes presented as string columns on the raw DataFrame
    2. Extact date attributes from the order_purchase_ts column in
    order to get more information about customers behavior on buying online.

    Examples:
        ```python
        df_orders_prep = transform_orders(df=df_orders)
        ```

    Args:
        df (DataFrame): A Spark DataFrame where transformations will be applied

    Returns:
        A new Spark DataFrame with a mapped transformation DAG.
    """

    logger.info("Preparing a transformation DAG for df_orders DataFrame")
    try:
        # Creating a list of date attributes do be casted
        date_cols = [
            "order_purchase_ts",
            "order_approved_at",
            "order_deliv_carrier_dt",
            "order_deliv_customer_dt",
            "order_estim_deliv_dt"
        ]

        # Defining a common date format
        date_fmt = "dd/MM/yyyy HH:mm"

        # Iterating over date cols and calling a sparksnake method
        df_orders_date_cast = df
        for date_col in date_cols:
            df_orders_date_cast = SparkETLManager.date_transform(
                df=df_orders_date_cast,
                date_col=date_col,
                date_col_type="timestamp",
                convert_string_to_date=True,
                date_format=date_fmt
            )

        # Extracting date attributes from order purchase date
        df_orders_prep = SparkETLManager.date_transform(
            df=df_orders_date_cast,
            date_col="order_purchase_ts",
            convert_string_to_date=False,
            year=True,
            quarter=True,
            month=True,
            dayofmonth=True,
            dayofweek=True,
            dayofyear=True,
            weekofyear=True
        )

        # Selecting attributes
        df_orders_prep = df_orders_prep.selectExpr(
            "order_id",
            "customer_id",
            "order_status",
            "order_approved_at",
            "order_deliv_carrier_dt",
            "order_deliv_customer_dt",
            "order_estim_deliv_dt",
            "order_purchase_ts",
            "year_order_purchase_ts",
            "quarter_order_purchase_ts",
            "month_order_purchase_ts",
            "dayofmonth_order_purchase_ts",
            "dayofweek_order_purchase_ts",
            "dayofyear_order_purchase_ts",
            "weekofyear_order_purchase_ts"
        )

        return df_orders_prep

    except Exception as e:
        logger.error("Error on preparing a transformation DAG for orders "
                     f"dataset. Exception: {e}")
        raise e


# Transformation method: df_order_items
def transform_order_items(df: DataFrame) -> DataFrame:
    """Creates a DAG to transform order items data.

    This function is responsible for applying the business rules to the
    order_items DataFrame in order to create a new and prepared DataFrame
    object. Here are the steps taken:

    1. Group data by order_id to extract some statistics about item's price

    Examples:
        ```python
        df_order_items_prep = transform_order_items(df=df_order_items)
        ```

    Args:
        df (DataFrame): A Spark DataFrame where transformations will be applied

    Returns:
        A new Spark DataFrame with a mapped transformation DAG.
    """

    logger.info("Preparing a transformation DAG for df_order_items DataFrame")
    try:
        # Casting the shipping limit column to timestamp
        df_order_items_stats = df.groupBy("order_id").agg(
            count("product_id").alias("qty_order_items"),
            round(sum("price"), 2).alias("sum_order_price"),
            round(mean("price"), 2).alias("mean_order_price"),
            round(max("price"), 2).alias("max_order_price"),
            round(min("price"), 2).alias("min_order_price"),
            round(mean("freight_value"), 2).alias("mean_order_freight_value"),
        )

        # Selecting attributes
        df_order_items_prep = df_order_items_stats.selectExpr(
            "order_id",
            "qty_order_items",
            "sum_order_price",
            "mean_order_price",
            "max_order_price",
            "min_order_price",
            "mean_order_freight_value"
        )

        return df_order_items_prep

    except Exception as e:
        logger.error("Error on preparing a transformation DAG for order_items "
                     f"dataset. Exception: {e}")
        raise e


# Transformation method: df_customers
def transform_customers(df: DataFrame) -> DataFrame:
    """Creates a DAG to transform customers data.

    This function is responsible for applying the business rules to the
    customers DataFrame in order to create a new and prepared DataFrame
    object. Here are the steps taken:

    1. Select some columns from the raw DataFrame

    Examples:
        ```python
        df_customers_prep = transform_customers(df=df_customers)
        ```

    Args:
        df (DataFrame): A Spark DataFrame where transformations will be applied

    Returns:
        A new Spark DataFrame with a mapped transformation DAG.
    """

    logger.info("Preparing a transformation DAG for df_customers DataFrame")
    try:
        df_customers_prep = df.selectExpr(
            "customer_id",
            "customer_city",
            "customer_state"
        )

        return df_customers_prep

    except Exception as e:
        logger.error("Error on preparing a transformation DAG for customers "
                     f"dataset. Exception: {e}")
        raise e


# Transformation method: df_payments
def transform_payments(
    df: DataFrame,
    spark_session: SparkSession
) -> DataFrame:
    """Creates a DAG to transform payments data.

    This function is responsible for applying the business rules to the
    payments DataFrame in order to create a new and prepared DataFrame
    object. Here are the steps taken:

    1. Find the most common payment method by counting rows and grouping
    by order_id and payment_type, sorting the result by the count column
    and dropping duplicates
    2. Aggregate data in order to find total installments, sum of payments,
    mean of payments and the distinct number of payment types
    3. Join the two temporary DataFrames from steps 1 and 2 to create a
    third and final one with selected attributes

    Examples:
        ```python
        df_payments_prep = transform_payments(df=df_payments)
        ```

    Args:
        df (DataFrame): A Spark DataFrame where transformations will be applied

    Returns:
        A new Spark DataFrame with a mapped transformation DAG.
    """

    logger.info("Preparing a transformation DAG for df_payments DataFrame")
    try:
        # Getting the most common payment type for each order_id
        df_common_payments = df.groupBy("order_id", "payment_type")\
            .count()\
            .sort(col("count").desc(), "payment_type")\
            .dropDuplicates(["order_id"])\
            .withColumnRenamed("payment_type", "most_common_payment_type")\
            .drop("count")

        # Extracting some statistical attributes from the raw data
        df_payments_aggreg = SparkETLManager.agg_data(
            df=df,
            spark_session=spark_session,
            group_by="order_id",
            agg_col="payment_value",
            round_result=True,
            n_round=2,
            count=True,
            sum=True,
            mean=True
        )

        # Joining both DataFrames
        df_payments_join = df_payments_aggreg.join(
            other=df_common_payments,
            on=[df_payments_aggreg.order_id == df_common_payments.order_id],
            how="left"
        ).drop(df_common_payments.order_id)

        # Modifying the column order to get a final transformation DAG
        df_payments_prep = df_payments_join.select(
            "order_id",
            "sum_payment_value",
            "mean_payment_value",
            "count_payment_value",
            "most_common_payment_type"
        )

        return df_payments_prep

    except Exception as e:
        logger.error("Error on preparing a transformation DAG for payments "
                     f"dataset. Exception: {e}")
        raise e


# Transformation method: df_reviews
def transform_reviews(df: DataFrame) -> DataFrame:
    """Creates a DAG to transform reviews data.

    This function is responsible for applying the business rules to the
    reviews DataFrame in order to create a new and prepared DataFrame
    object. Here are the steps taken:

    1. Filter only reviews with order_id not null and a valid score number
    2. Select and casting some useful fields
    3. Group data by order_id and aggregate the score information to get
    the best score and a unique comment message for each id
    4. Drop duplicates on order_id field

    Examples:
        ```python
        df_reviews_prep = transform_reviews(df=df_reviews)
        ```

    Args:
        df (DataFrame): A Spark DataFrame where transformations will be applied

    Returns:
        A new Spark DataFrame with a mapped transformation DAG.
    """

    logger.info("Preparing a transformation DAG for df_reviews DataFrame")
    try:
        # Applying filters to remove invalid data
        df_reviews_filtered = df\
            .where("order_id is not null")\
            .where("length(review_score) = 1")

        # Getting the best score for each order_id
        df_reviews_prep = df_reviews_filtered.select(
            col("order_id"),
            col("review_score").cast("int"),
            col("review_comment_message")
        ).groupBy("order_id").agg(
            max("review_score").alias("review_best_score"),
            max("review_comment_message").alias("review_comment_message")
        ).drop_duplicates(["order_id"])

        return df_reviews_prep

    except Exception as e:
        logger.error("Error on preparing a transformation DAG for reviews "
                     f"dataset. Exception: {e}")
        raise e


# Transformation method: joining all datasets
def transform_sot(**kwargs) -> DataFrame:
    """Creates a DAG to transform the SoT dataset.

    This function is responsible for joining all transformed DataFrames in
    order to create a single DataFrame object with all required data. The
    transformation step considers applying multiple joins using the
    df_orders_prep DataFrames as a main collection from left joining on
    all other DataFrames.

    In the end, a select statement will ensure that all fields match the
    expected schema for the SoT table.

    Examples:
        ```python
        df_sot = transform_sot(
            df_orders_prep=df_orders_prep,
            df_order_items_prep=df_order_items_prep,
            df_customers_prep=df_customers_prep,
            df_payments_prep=df_payments_prep,
            df_reviews_prep=df_reviews_prep
        )
        ```

    Keyword Args:
        df_orders_prep (DataFrame):
            A prepared Spark DataFrame for tbl_orders

        df_order_items_prep (DataFrame):
            A prepared Spark DataFrame for tbl_order_items

        df_customers_prep (DataFrame):
            A prepared Spark DataFrame for tbl__customers

        df_payments_prep (DataFrame):
            A prepared Spark DataFrame for tbl_payments

        df_reviews_prep (DataFrame):
            A prepared Spark DataFrame for tbl_reviews

    Returns:
        A new Spark DataFrame with a mapped transformation DAG.
    """

    # Getting individual DataFrames from kwargs
    df_orders_prep = kwargs["df_orders_prep"]
    df_order_items_prep = kwargs["df_order_items_prep"]
    df_customers_prep = kwargs["df_customers_prep"]
    df_payments_prep = kwargs["df_payments_prep"]
    df_reviews_prep = kwargs["df_reviews_prep"]

    logger.info("Preparing a transformation DAG for SoT DataFrame")
    try:
        # Joining all the prepared DataFrames
        df_sot_join = df_orders_prep.join(
            other=df_order_items_prep,
            on=[df_orders_prep.order_id == df_order_items_prep.order_id]
        ).drop(df_order_items_prep.order_id).join(
            other=df_customers_prep,
            on=[df_orders_prep.customer_id == df_customers_prep.customer_id],
            how="left"
        ).drop(df_customers_prep.customer_id).join(
            other=df_payments_prep,
            on=[df_orders_prep.order_id == df_payments_prep.order_id],
            how="left"
        ).drop(df_payments_prep.order_id).join(
            other=df_reviews_prep,
            on=[df_orders_prep.order_id == df_reviews_prep.order_id],
            how="left"
        ).drop(df_reviews_prep.order_id)

        # Selecting final attributes
        df_sot_prep = df_sot_join.selectExpr(
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_ts",
            "order_approved_at",
            "order_deliv_carrier_dt",
            "order_deliv_customer_dt",
            "order_estim_deliv_dt",
            "year_order_purchase_ts",
            "quarter_order_purchase_ts",
            "month_order_purchase_ts",
            "dayofmonth_order_purchase_ts",
            "dayofweek_order_purchase_ts",
            "dayofyear_order_purchase_ts",
            "weekofyear_order_purchase_ts",
            "qty_order_items",
            "sum_order_price",
            "mean_order_price",
            "max_order_price",
            "min_order_price",
            "mean_order_freight_value",
            "customer_city",
            "customer_state",
            "sum_payment_value",
            "mean_payment_value",
            "count_payment_value",
            "most_common_payment_type",
            "review_best_score",
            "review_comment_message"
        )

    except Exception as e:
        logger.error("Error on preparing a transformation DAG for SoT "
                     f"dataset. Exception: {e}")
        raise e

    # Retornando base final
    return df_sot_prep
