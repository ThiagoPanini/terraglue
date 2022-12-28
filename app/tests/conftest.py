"""
SCRIPT: conftest.py

CONTEXTO:
---------
Arquivo de conferência/configuração do pytest para
alocação de fixtures e outros elementos e insumos
utilizados durante a execução dos testes.

OBJETIVO:
---------
Centralizar os insumos utilizados na execução da suíte
de testes do projeto.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Importando módulos para uso
from pytest import fixture
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType
from tests.utils.spark_helper import generate_fake_spark_dataframe,\
    create_spark_session


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
        1.2 Definição de variáveis e objetos
---------------------------------------------------"""

# Definindo variáveis de definição dos DataFrames
SCHEMA_DTYPE = StringType()
NULLABLE = True
NUM_ROWS = 5

# Schema para criação de DataFrame: customers
SCHEMA_CUSTOMERS = [
    "customer_id",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state"
]

# Schema para criação de DataFrame: orders
SCHEMA_ORDERS = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

# Schema para criação de DataFrame: payments
SCHEMA_PAYMENTS = [
    "order_id",
    "payment_sequential",
    "payment_type",
    "payment_installments",
    "payment_value"
]

# Schema para criação de DataFrame: reviews
SCHEMA_REVIEWS = [
    "review_id",
    "order_id",
    "review_score",
    "review_comment_title",
    "review_comment_message",
    "review_creation_date",
    "review_answer_timestamp"
]


"""---------------------------------------------------
---------- 2. INSUMOS E ELEMENTOS DO PYTEST ----------
              2.1 Definição de fixtures
---------------------------------------------------"""


# Fixture para entregar um objeto de sessão Spark
@fixture()
def spark():
    return create_spark_session()


# Fixture para entregar um DataFrame Spark: customers
@fixture()
def df_customers(spark: SparkSession,
                 schema_input=SCHEMA_CUSTOMERS,
                 schema_dtype=SCHEMA_DTYPE,
                 nullable=NULLABLE,
                 num_rows=NUM_ROWS):

    return generate_fake_spark_dataframe(
        spark=spark,
        schema_input=schema_input,
        schema_dtype=schema_dtype,
        nullable=nullable,
        num_rows=num_rows
    )


# Fixture para entregar um DataFrame Spark: orders
@fixture()
def df_orders(spark: SparkSession,
              schema_input=SCHEMA_ORDERS,
              schema_dtype=SCHEMA_DTYPE,
              nullable=NULLABLE,
              num_rows=NUM_ROWS):

    return generate_fake_spark_dataframe(
        spark=spark,
        schema_input=schema_input,
        schema_dtype=schema_dtype,
        nullable=nullable,
        num_rows=num_rows
    )


# Fixture para entregar um DataFrame Spark: payments
@fixture()
def df_payments(spark: SparkSession,
                schema_input=SCHEMA_PAYMENTS,
                schema_dtype=SCHEMA_DTYPE,
                nullable=NULLABLE,
                num_rows=NUM_ROWS):

    return generate_fake_spark_dataframe(
        spark=spark,
        schema_input=schema_input,
        schema_dtype=schema_dtype,
        nullable=nullable,
        num_rows=num_rows
    )


# Fixture para entregar um DataFrame Spark: reviews
@fixture()
def df_reviews(spark: SparkSession,
               schema_input=SCHEMA_REVIEWS,
               schema_dtype=SCHEMA_DTYPE,
               nullable=NULLABLE,
               num_rows=NUM_ROWS):

    return generate_fake_spark_dataframe(
        spark=spark,
        schema_input=schema_input,
        schema_dtype=schema_dtype,
        nullable=nullable,
        num_rows=num_rows
    )
