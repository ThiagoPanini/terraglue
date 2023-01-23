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
import sys
import os

import pytest
from faker import Faker

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType

from src.main import ARGV_LIST, DATA_DICT, GlueTransformationManager
from src.terraglue import GlueJobManager, GlueETLManager

from tests.helpers.iac_helper import extract_map_variable_from_ferraform
from tests.helpers.spark_helper import generate_fake_spark_dataframe

from tests.configs.inputs import JOB_REQUIRED_ARGS, TF_VAR_NAME_JOB_ARGS,\
    JOB_RUNTIME_ARGS, DATA_DICT_REQUIRED_KEYS, FAKE_DATAFRAME_SCHEMA


# Instanciando objeto Faker
faker = Faker()
Faker.seed(42)


"""---------------------------------------------------
----------- 2. DEFINIÇÃO DE FIXTURES ÚTEIS -----------
     2.1 Fixtures utilizadas em test_user_inputs
---------------------------------------------------"""


# Variável ARGV_LIST definida no código da aplicação
@pytest.fixture()
def argv_list() -> list:
    return ARGV_LIST


# Lista drgumentos obrigatórios definidos pelo usuário
@pytest.fixture()
def user_required_args() -> list:
    return JOB_REQUIRED_ARGS


# Dicionário de argumentos definidos pelo usuário no Terraform
@pytest.fixture()
def iac_job_user_args() -> dict:
    return extract_map_variable_from_ferraform(
        var_name=TF_VAR_NAME_JOB_ARGS
    )


# Lista de argumentos do job criados apenas em tempo de execução
@pytest.fixture()
def job_runtime_args() -> list:
    return JOB_RUNTIME_ARGS


# Variável DATA_DICT definida no código da aplicação
@pytest.fixture()
def data_dict() -> dict:
    return DATA_DICT


# Lista de chaves obrigatórias da variável DATA_DICT
@pytest.fixture()
def required_data_dict_keys() -> list:
    return DATA_DICT_REQUIRED_KEYS


"""---------------------------------------------------
----------- 2. DEFINIÇÃO DE FIXTURES ÚTEIS -----------
     2.2 Fixtures utilizadas em test_job_manager
---------------------------------------------------"""


# Argumentos do job utilizados para instância de classe para testes
@pytest.fixture()
def job_args_for_testing(iac_job_user_args, job_runtime_args) -> dict:
    # Simulando argumentos obtidos apenas em tempo de execução
    iac_job_user_args_complete = dict(iac_job_user_args)
    for arg in job_runtime_args:
        iac_job_user_args_complete[arg] = faker.word()

    return iac_job_user_args_complete


# Objeto instanciado da classe GlueJobManager
@pytest.fixture()
def job_manager(job_args_for_testing) -> GlueJobManager:
    # Adicionando argumentos ao vetor de argumentos do sistema
    for arg_name, arg_value in job_args_for_testing.items():
        sys.argv.append(f"--{arg_name}={arg_value}")

    job_manager = GlueJobManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT
    )

    return job_manager


"""---------------------------------------------------
----------- 2. DEFINIÇÃO DE FIXTURES ÚTEIS -----------
      2.3 Fixtures utilizadas em test_etl_manager
---------------------------------------------------"""


# Objeto de sessão Spark para uso genérico
@pytest.fixture()
def spark():
    return SparkSession.builder.getOrCreate()


# Objeto instanciado da classe GlueETLManager
@pytest.fixture()
def etl_manager(job_args_for_testing):
    # Adicionando argumentos ao vetor de argumentos
    for arg_name, arg_value in job_args_for_testing.items():
        sys.argv.append(f"--{arg_name}={arg_value}")

    # Instanciando objeto
    etl_manager = GlueETLManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT
    )

    return etl_manager


# Resultado da execução do método generate_dynamic_frames_dict
@pytest.fixture()
def dyf_dict(etl_manager):
    etl_manager.init_job()
    return etl_manager.generate_dynamic_frames_dict()


# DataFrame fake para testagem de transformações Spark
@pytest.fixture()
def fake_dataframe(spark):
    return generate_fake_spark_dataframe(
        spark=spark,
        schema_input=FAKE_DATAFRAME_SCHEMA
    )


"""---------------------------------------------------
----------- 2. DEFINIÇÃO DE FIXTURES ÚTEIS -----------
        2.4 Fixtures utilizadas em test_main
---------------------------------------------------"""


# Objeto instanciado da classe GlueETLManager
@pytest.fixture()
def glue_manager(job_args_for_testing):
    # Adicionando argumentos ao vetor de argumentos
    for arg_name, arg_value in job_args_for_testing.items():
        sys.argv.append(f"--{arg_name}={arg_value}")

    glue_manager = GlueTransformationManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT
    )

    return glue_manager


# DataFrame vazio para teste de exceção dos métodos de transformação
@pytest.fixture()
def empty_df(spark):
    # Criando RDD e schema vazios
    empty_rdd = spark.sparkContext.emptyRDD()
    empty_schema = StructType()

    # Criando e retornando DataFrame vazio
    return spark.createDataFrame(data=empty_rdd, schema=empty_schema)


# Amostra de DataFrame df_orders
@pytest.fixture()
def df_orders(spark):
    # Definindo variável para leitura do DataFrame
    filename = "sample_olist_orders_dataset.csv"
    data_path = os.path.join(
        os.getcwd(),
        f"app/tests/samples/{filename}"
    )

    # Realizando a leitura do DataFrame
    df = spark.read.format("csv")\
        .option("header", "true")\
        .option("inferSchema", "false")\
        .load(data_path)

    return df


# Resultado do método de transformação df_orders_prep
@pytest.fixture()
def df_orders_prep(glue_manager, df_orders):
    return glue_manager.transform_orders(df_orders)


# Amostra de DataFrame df_order_items
@pytest.fixture()
def df_order_items(spark):
    # Definindo variável para leitura do DataFrame
    filename = "sample_olist_order_items_dataset.csv"
    data_path = os.path.join(
        os.getcwd(),
        f"app/tests/samples/{filename}"
    )

    # Realizando a leitura do DataFrame
    df = spark.read.format("csv")\
        .option("header", "true")\
        .option("inferSchema", "false")\
        .load(data_path)

    return df


# Resultado do método de transformação df_order_items_prep
@pytest.fixture()
def df_order_items_prep(glue_manager, df_order_items):
    return glue_manager.transform_order_items(df_order_items)


# Amostra de DataFrame df_customers
@pytest.fixture()
def df_customers(spark):
    # Definindo variável para leitura do DataFrame
    filename = "sample_olist_customers_dataset.csv"
    data_path = os.path.join(
        os.getcwd(),
        f"app/tests/samples/{filename}"
    )

    # Realizando a leitura do DataFrame
    df = spark.read.format("csv")\
        .option("header", "true")\
        .option("inferSchema", "false")\
        .load(data_path)

    return df


# Resultado do método de transformação df_customers_prep
@pytest.fixture()
def df_customers_prep(glue_manager, df_customers):
    return glue_manager.transform_customers(df_customers)


# Amostra de DataFrame df_payments
@pytest.fixture()
def df_payments(spark):
    # Definindo variável para leitura do DataFrame
    filename = "sample_olist_order_payments_dataset.csv"
    data_path = os.path.join(
        os.getcwd(),
        f"app/tests/samples/{filename}"
    )

    # Realizando a leitura do DataFrame
    df = spark.read.format("csv")\
        .option("header", "true")\
        .option("inferSchema", "false")\
        .load(data_path)

    return df


# Resultado do método de transformação df_payments_prep
@pytest.fixture()
def df_payments_prep(glue_manager, df_payments):
    return glue_manager.transform_payments(df_payments)


# Amostra de DataFrame df_reviews
@pytest.fixture()
def df_reviews(spark):
    # Definindo variável para leitura do DataFrame
    filename = "sample_olist_order_reviews_dataset.csv"
    data_path = os.path.join(
        os.getcwd(),
        f"app/tests/samples/{filename}"
    )

    # Realizando a leitura do DataFrame
    df = spark.read.format("csv")\
        .option("header", "true")\
        .option("inferSchema", "false")\
        .load(data_path)

    return df


# Resultado do método de transformação df_reviews_prep
@pytest.fixture()
def df_reviews_prep(glue_manager, df_reviews):
    return glue_manager.transform_reviews(df_reviews)


# Resultado do método de transformação df_sot_prep
@pytest.fixture()
def df_sot_prep(glue_manager, df_orders_prep, df_order_items_prep,
                df_customers_prep, df_payments_prep,
                df_reviews_prep):
    return glue_manager.transform_sot(
        df_orders_prep=df_orders_prep,
        df_order_items_prep=df_order_items_prep,
        df_customers_prep=df_customers_prep,
        df_payments_prep=df_payments_prep,
        df_reviews_prep=df_reviews_prep
    )
