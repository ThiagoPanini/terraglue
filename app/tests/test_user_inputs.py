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


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


@mark.user_input
def test_tipo_primitivo_variavel_argvlist(argv_list):
    """
    G: dado que o usuário iniciou a codificação do seu job Glue
    W: quando o usuário definir a variável ARGV_LIST
    T: então esta deve ser do tipo list
    """
    assert type(argv_list) == list


@mark.user_input
def test_variavel_argvlist_possui_argumentos(argv_list):
    """
    G: dado que o usuário iniciou a codificação do seu job Glue
    W: quando o usuário definir a variável ARGV_LIST
    T: então esta deve possuir pelo menos 1 elemento
    """
    assert len(argv_list) >= 1


@mark.user_input
def test_variavel_argvlist_possui_argumentos_obrigatorios(argv_list,
                                                          required_args):
    """
    G: dado que o usuário iniciou a codificação do seu job Glue
    W: quando o usuário definir a variável ARGV_LIST
    T: então esta deve possuir uma série argumentos obrigatórios
    """
    assert all(arg in argv_list for arg in required_args)


@mark.user_input
def test_tipo_primitivo_variavel_datadict(data_dict):
    """
    G: dado que o usuário iniciou a codificação do seu job Glue
    W: quando o usuário definir a variável DATA_DICT
    T: então esta deve ser do tipo dict
    """
    assert type(data_dict) == dict


@mark.user_input
def test_variavel_datadict_possui_elementos(data_dict):
    """
    G: dado que o usuário iniciou a codificação do seu job Glue
    W: quando o usuário definir a variável DATA_DICT
    T: então esta deve possuir pelo menos 1 elemento
    """
    assert len(data_dict) >= 1


@mark.user_input
def test_variavel_datadict_possui_chaves_obrigatorias(data_dict,
                                                      required_data_dict_keys):
    """
    G: dado que o usuário iniciou a codificação do seu job Glue
    W: quando o usuário definir a variável DATA_DICT
    T: então esta deve possuir algumas chaves obrigatórias em sua definição
    """

    # Extraindo chaves do dicionário
    data_dict_keys = [list(data_dict[t].keys()) for t in data_dict.keys()]

    # Iterando sobre lista de listas e validando
    for keys in data_dict_keys:
        assert all(key in keys for key in required_data_dict_keys)
