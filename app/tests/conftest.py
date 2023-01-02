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
from tests.utils.iac_helper import extract_map_variable_from_ferraform
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

    job = GlueJobManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT
    )

    return job
