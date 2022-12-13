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
from pytest import mark
from pyspark.sql import DataFrame


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


def test_geracao_de_dataframe_spark_df_customers(df_customers):
    """
    Given:
    When:
    Then:
    """

    assert type(df_customers) == DataFrame