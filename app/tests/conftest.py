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
from pytest import fixture
from src.main import ARGV_LIST, DATA_DICT
from src.terraglue import GlueJobManager


"""---------------------------------------------------
----------- 2. DEFINIÇÃO DE FIXTURES ÚTEIS -----------
     2.1 Fixtures utilizadas em test_user_inputs
---------------------------------------------------"""


@fixture()
def argv_list():
    return ARGV_LIST


@fixture()
def user_required_args():
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


@fixture()
def data_dict():
    return DATA_DICT


@fixture()
def required_data_dict_keys():
    return [
        "database",
        "table_name",
        "transformation_ctx"
    ]


"""---------------------------------------------------
----------- 2. DEFINIÇÃO DE FIXTURES ÚTEIS -----------
     2.2 Fixtures utilizadas em test_job_manager
---------------------------------------------------"""


@fixture()
def job_args():
    return {
        "JOB_NAME": "gluejob-sot-ecommerce-br",
        "OUTPUT_BUCKET": "teste",
        "OUTPUT_DB": "ra8",
        "OUTPUT_TABLE": "tbsot_ecommerce_br",
        "CONNECTION_TYPE": "s3",
        "UPDATE_BEHAVIOR": "UPDATE_IN_DATABASE",
        "PARTITION_NAME": "anomesdia",
        "PARTITION_FORMAT": "%Y%m%d",
        "DATA_FORMAT": "parquet",
        "COMPRESSION": "snappy",
        "ENABLE_UPDATE_CATALOG": "True",
        "NUM_PARTITIONS": 5
    }


@fixture()
def job_manager(job_args):
    # Adicionando argumentos ao vetor de argumentos
    for arg_name, arg_value in job_args.items():
        sys.argv.append(f"--{arg_name}={arg_value}")

    job = GlueJobManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT
    )

    return job
