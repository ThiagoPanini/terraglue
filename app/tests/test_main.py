"""
SCRIPT: test_main.py

CONTEXTO:
---------
Script de testes criado para validar as principais
funcionalidades da aplicação Spark desenvolvida e
consolidada através do script main-terraglue.py
disponibilizado no diretório ./app/src do projeto.
Como a aplicação envolve um job Spark executado no
serviço AWS Glue, o grande desafio em desenvolver
uma suíte de testes está relacionado a forma de
simulação do processo de execução do job.

OBJETIVO:
---------
Consoldar uma suíte de testes capaz de testar e validar
as principais funcionalidades da aplicação Spark
do projeto.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Importando módulos para uso
from pyspark.sql import DataFrame
from pytest import mark
from src.main import ARGV_LIST, DATA_DICT


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


def test_tipo_primitivo_da_variavel_argvlist():
    """
    G:
    W:
    T:
    """
    assert type(ARGV_LIST) == list


def test_tipo_primitivo_da_variavel_datadict():
    """
    G:
    W:
    T:
    """
    assert type(DATA_DICT) == dict


@mark.dataframes
def test_tipo_primitivo_de_dataframes_spark_gerados_na_fixture(
    df_customers, df_orders, df_payments, df_reviews
):
    """
    G: dado que o usuário queira criar um DataFrame para uma base
    W: quando a função de criação de DataFrames for executada na fixture
    T: o tipo primitivo do retorno deve ser um DatataFrame Spark
    """

    assert type(df_customers) == DataFrame
    assert type(df_orders) == DataFrame
    assert type(df_payments) == DataFrame
    assert type(df_reviews) == DataFrame
