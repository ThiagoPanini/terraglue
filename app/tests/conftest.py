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
from faker import Faker
from pyspark.sql import SparkSession
from pyspark.sql.types import *


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
        1.2 Definição de variáveis e objetos
---------------------------------------------------"""

# Inicializando faker para geração de dados fictícios
faker = Faker()

# Schema para criação de DataFrame: customers
DF_CUSTOMERS_COLUMNS= [
    "customer_id","customer_unique_id", "customer_zip_code_prefix",
    "customer_city","customer_state"
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
                 columns:list=DF_CUSTOMERS_COLUMNS,
                 all_string:bool=True):
    """
    """
    # Gerando schema
    if all_string:
        schema = StructType([
            StructField(col, StringType(), nullable=True)
            for col in columns
        ])

        # Faking data
        data = [(faker.word()) for i in range(len(schema))]

    # Criando DataFrame Spark
    return spark.createDataFrame(data, schema)

