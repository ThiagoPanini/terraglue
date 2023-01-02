"""
SCRIPT: test_user_inputs.py

CONTEXTO:
---------
Script de testes criado para validar elementos e
funcionalidades presentes na classe GlueJobManager do
módulo terraglue como forma de garantir que todos os
insumos necessários para execução da aplicação Spark
se fazem presentes.

OBJETIVO:
---------
Consoldar uma suíte de testes capaz de testar e validar
todos os insumos presentes na classe GlueJobManager que
podem comprometer o funcionamento da aplicação.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Importando módulos para uso
from pytest import mark


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


@mark.job_manager
def test_captura_de_argumentos_do_job_na_construcao_da_classe(job_manager,
                                                              job_args):
    """
    G: dado que o usuário instanciou um objeto da classe Job Manager
    W: quando o método construtor da classe for executado
    T: os argumentos passados pelo usuário devem estar contidos no
       dicionário de argumentos gerais do job gerado a partir do método
       awsglue.utilsgetResolverOptions como um subset do mesmo.
    """

    # Corrigindo argumentos convertidos automaticamente em string
    job_manager.args["NUM_PARTITIONS"] = int(job_manager.args["NUM_PARTITIONS"])

    assert job_args.items() <= job_manager.args.items()

