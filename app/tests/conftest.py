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
from pytest import fixture
from src.main import ARGV_LIST, DATA_DICT, GlueTransformationManager
from src.terraglue import GlueJobManager, GlueETLManager
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType,\
    IntegerType, DateType, TimestampType
from tests.utils.iac_helper import extract_map_variable_from_ferraform
from tests.utils.spark_helper import generate_fake_spark_dataframe
from faker import Faker


# Instanciando objeto Faker
faker = Faker()
Faker.seed(42)


"""---------------------------------------------------
----------- 2. DEFINIÇÃO DE FIXTURES ÚTEIS -----------
     2.1 Fixtures utilizadas em test_user_inputs
---------------------------------------------------"""


# Variável ARGV_LIST definida no código da aplicação
@fixture()
def argv_list() -> list:
    return ARGV_LIST


# Lista drgumentos obrigatórios definidos pelo usuário
@fixture()
def user_required_args() -> list:
    return [
        "JOB_NAME",
        "OUTPUT_BUCKET",
        "OUTPUT_DB",
        "OUTPUT_TABLE",
        "CONNECTION_TYPE",
        "UPDATE_BEHAVIOR",
        "DATA_FORMAT",
        "COMPRESSION",
        "ENABLE_UPDATE_CATALOG"
    ]


# Dicionário de argumentos definidos pelo usuário no Terraform
@fixture()
def iac_job_user_args() -> dict:
    return extract_map_variable_from_ferraform(
        var_name="glue_job_user_arguments"
    )


# Lista de argumentos do job criados apenas em tempo de execução
@fixture()
def job_runtime_args() -> list:
    return ["JOB_NAME", "OUTPUT_BUCKET"]


# Variável DATA_DICT definida no código da aplicação
@fixture()
def data_dict() -> dict:
    return DATA_DICT


# Lista de chaves obrigatórias da variável DATA_DICT
@fixture()
def required_data_dict_keys() -> list:
    return [
        "database",
        "table_name",
        "transformation_ctx"
    ]


"""---------------------------------------------------
----------- 2. DEFINIÇÃO DE FIXTURES ÚTEIS -----------
     2.2 Fixtures utilizadas em test_job_manager
---------------------------------------------------"""


# Argumentos do job utilizado para instância de classe para testes
@fixture()
def job_args_for_testing(iac_job_user_args, job_runtime_args) -> dict:
    # Simulando argumentos obtidos apenas em tempo de execução
    iac_job_user_args_complete = dict(iac_job_user_args)
    for arg in job_runtime_args:
        iac_job_user_args_complete[arg] = faker.word()

    return iac_job_user_args_complete


# Objeto instanciado da classe GlueJobManager
@fixture()
def job_manager(job_args_for_testing) -> GlueJobManager:
    # Adicionando argumentos ao vetor de argumentos
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
@fixture()
def spark():
    return SparkSession.builder.getOrCreate()


# Objeto instanciado da classe GlueETLManager
@fixture()
def etl_manager(job_args_for_testing):
    # Adicionando argumentos ao vetor de argumentos
    for arg_name, arg_value in job_args_for_testing.items():
        sys.argv.append(f"--{arg_name}={arg_value}")

    etl_manager = GlueETLManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT
    )

    return etl_manager


# DataFrame fake para testagem de transformações Spark
@fixture()
def fake_dataframe(spark):
    # Definindo schema para DataFrame fictício
    schema = StructType([
        StructField("id", StringType()),
        StructField("value", IntegerType()),
        StructField("date", DateType()),
        StructField("timestamp", TimestampType())
    ])

    # Gerando DataFrame fictício
    return generate_fake_spark_dataframe(
        spark=spark,
        schema_input=schema
    )


"""---------------------------------------------------
----------- 2. DEFINIÇÃO DE FIXTURES ÚTEIS -----------
        2.4 Fixtures utilizadas em test_main
---------------------------------------------------"""


# Objeto instanciado da classe GlueETLManager
@fixture()
def glue_manager(job_args_for_testing):
    # Adicionando argumentos ao vetor de argumentos
    for arg_name, arg_value in job_args_for_testing.items():
        sys.argv.append(f"--{arg_name}={arg_value}")

    glue_manager = GlueTransformationManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT
    )

    return glue_manager


# Amostra de DataFrame df_orders
@fixture()
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


# Resultado do método de transformação do DataFrame df_orders
@fixture()
def df_orders_prep(glue_manager, df_orders):
    return glue_manager.transform_orders(df_orders)