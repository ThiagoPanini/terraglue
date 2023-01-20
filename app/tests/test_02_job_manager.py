"""
SCRIPT: test_job_manager.py

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
import pytest
from pytest import mark
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from pyspark.sql import SparkSession
from awsglue.job import Job


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


@mark.job_manager
def test_captura_de_argumentos_do_job_na_construcao_da_classe(
    job_manager,
    job_args_for_testing
):
    """
    G: dado que o usuário instanciou um objeto da classe Job Manager
    W: quando o método construtor da classe for executado
    T: os argumentos passados pelo usuário no ato de criação de objeto
       devem estar contidos no dicionário de argumentos gerais do job
       obtidos, na classe, a partir do método awsglue.utilsgetResolverOptions
    """
    assert job_args_for_testing.items() <= job_manager.args.items()


@mark.job_manager
def test_erro_ao_executar_metodo_print_args(job_manager):
    """
    G: dado que o usuário inicializou o objeto job_manager com
       algum argumento de sistema nulo
    W: quando o método print_args() for executado
    T: então uma exceção deve ser lançada
    """
    # Modificando argumentos do sistema salvos no objeto da classe
    job_manager.args = None

    with pytest.raises(Exception):
        # Chamando método para print de argumentos no log
        job_manager.print_args()


@mark.job_manager
def test_obtencao_de_elementos_de_contexto_e_sessao(job_manager):
    """
    G: dado que o usuário deseja obter os elementos de contexto e sessão no Job
    W: quando o método get_context_and_session() for executado
    T: então os atributos self.sc, self.glueContext e self.spark devem existir
       na classe GlueJobManager
    """

    # Executando método de coleta de elementos de contexto e sessão do job
    job_manager.get_context_and_session()

    # Coletando atributos da classe e definindo lista de validação
    class_attribs = job_manager.__dict__
    attribs_names = ["sc", "glueContext", "spark"]

    # Validando existência de atributos da classe
    assert all(a in list(class_attribs.keys()) for a in attribs_names)


@mark.job_manager
def test_tipos_primitivos_de_elementos_de_contexto_e_sessao(job_manager):
    """
    G: dado que o usuário deseja obter os elementos de contexto e sessão no Job
    W: quando o método get_context_and_session() for executado
    T: então os atributos self.sc, self.glueContext e self.spark devem
       representar elementos do tipo SparkContext, GlueContext e SparkSession,
       respectivamente
    """
    # Executando método de coleta de elementos de contexto e sessão do job
    job_manager.get_context_and_session()

    # Coletando atributos da classe e definindo lista de validação
    class_attribs = job_manager.__dict__

    # Validando tipos primitivos dos atributos de contexto e sessão
    assert type(class_attribs["sc"]) == SparkContext
    assert type(class_attribs["glueContext"]) == GlueContext
    assert type(class_attribs["spark"]) == SparkSession


@mark.job_manager
def test_metodo_de_inicializacao_do_job_gera_contexto_e_sessao(job_manager):
    """
    G: dado que deseja-se inicializar um job Glue pela classe GlueJobManager
    W: quando o método init_job() for chamado
    T: então os elementos de contexto e sessão (Spark e Glue) devem existir
       e apresentarem os tipos primitivos adequados
    """
    # Executando método de inicialização do job
    _ = job_manager.init_job()

    # Coletando atributos da classe e definindo lista de validação
    class_attribs = job_manager.__dict__
    attribs_names = ["sc", "glueContext", "spark"]

    # Validando existência de atributos da classe
    assert all(a in list(class_attribs.keys()) for a in attribs_names)

    # Validando tipos primitivos dos atributos de contexto e sessão
    assert type(class_attribs["sc"]) == SparkContext
    assert type(class_attribs["glueContext"]) == GlueContext
    assert type(class_attribs["spark"]) == SparkSession


@mark.job_manager
def test_metodo_de_inicializacao_do_job_retorna_tipo_job(job_manager):
    """
    G: dado que deseja-se inicializar um job Glue pela classe GlueJobManager
    W: quando o método init_job() for chamado
    T: então o retorno deve ser um objeto do tipo awsglue.job.Job
    """

    # Executando método de inicialização do job
    assert type(job_manager.init_job()) == Job
