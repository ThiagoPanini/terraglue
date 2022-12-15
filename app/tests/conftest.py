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
from utils.spark_helper import generate_spark_dataframe


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
        1.2 Definição de variáveis e objetos
---------------------------------------------------"""

# Inicializando sessão Spark
spark = SparkSession.builder\
    .appName("spark_helper")\
    .getOrCreate()

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


"""---------------------------------------------------
---------- 2. INSUMOS E ELEMENTOS DO PYTEST ----------
              2.1 Definição de fixtures
---------------------------------------------------"""


# Fixture para entregar um objeto de sessão Spark
@fixture()
def spark():
    return SparkSession.builder.getOrCreate()


# Fixture para entregar um DataFrame Spark: customers
@fixture()
def df_customers(spark: SparkSession,
                 schema_input=SCHEMA_CUSTOMERS,
                 schema_dtype=SCHEMA_DTYPE,
                 nullable=NULLABLE,
                 num_rows=NUM_ROWS):

    return generate_spark_dataframe(
        spark=spark,
        schema_input=schema_input,
        schema_dtype=schema_dtype,
        nullable=nullable,
        num_rows=num_rows
    )
