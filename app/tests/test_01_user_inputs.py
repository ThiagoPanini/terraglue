"""
SCRIPT: test_user_inputs.py

CONTEXTO:
---------
Script de testes criado para validar casos específicos
relacionados à definições de variáveis pelo usuário e
que são fundamentais para o funcionamento do código.

OBJETIVO:
---------
Consoldar uma suíte de testes capaz de testar e validar
entradas fornecidas pelo usuário que podem comprometer
o funcionamento de toda a aplicação.
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
@mark.argv_list
def test_variavel_argv_list_definida_como_uma_lista(argv_list):
    """
    G: dado que o usuário iniciou a codificação do seu job Glue
    W: quando a variável ARGV_LIST for definida/adaptada pelo usuário
    T: então esta deve ser uma lista do Python (tipo list)
    """
    assert type(argv_list) == list


@mark.user_input
@mark.argv_list
def test_variavel_argvlist_possui_argumentos_obrigatorios(argv_list,
                                                          user_required_args):
    """
    G: dado que o usuário iniciou a codificação do seu job Glue
    W: quando a variável ARGV_LIST for definida/adaptada pelo usuário
    T: então esta deve possuir uma série argumentos obrigatórios
    """
    assert all(arg in argv_list for arg in user_required_args)


@mark.user_input
@mark.argv_list
@mark.terraform
def test_variavel_argvlist_possui_argumentos_declarados_no_terraform(
    argv_list, iac_job_user_args, job_runtime_args
):
    """
    G: dado que o usuário definiu argumentos do job na ferramenta de IaC
    W: quando a variável ARGV_LIST for definida/adaptada pelo usuário
    T: então esta deve possuir os mesmos elementos/argumentos daqueles
       declarados na ferramenta de IaC (terraform), garantindo assim o
       processo de captura de todas as informações desejadas.

    Observação: o parâmetro "job_runtime_args" da função de teste contempla
    alguns argumentos que não são explicitamente declarados na ferramenta
    de IaC pelo usuário (arquivo variables.tf do Terraform) de forma
    direta. Isto pode acontecer pois existem argumentos do job que são
    definidos apenas em tempo de execução (ex: nome do bucket de saída
    que depende de um ID da conta e de um nome de região) ou então
    argumentos que existem apenas no ato de submissão do job Glue na
    AWS (ex: nome e ID do job)
    """

    # Obtendo lista de argumentos declaradas na ferramenta de IaC
    tf_args = list(iac_job_user_args.keys())

    # runtime_args ajuda a eliminar alguns parâmetros dinâmicos
    argv_list_custom = argv_list[:]
    for arg in job_runtime_args:
        argv_list_custom.remove(arg)

    assert set(argv_list_custom) == set(tf_args)


@mark.user_input
@mark.data_dict
def test_tipo_primitivo_variavel_datadict(data_dict):
    """
    G: dado que o usuário iniciou a codificação do seu job Glue
    W: quando a variável DATA_DICT for definida/adaptada pelo usuário
    T: então esta deve ser um dicionário do Python (tipo dict)
    """
    assert type(data_dict) == dict


@mark.user_input
@mark.data_dict
def test_variavel_datadict_possui_chaves_obrigatorias(data_dict,
                                                      required_data_dict_keys):
    """
    G: dado que o usuário iniciou a codificação do seu job Glue
    W: quando a variável DATA_DICT for definida/adaptada pelo usuário
    T: então esta deve possuir algumas chaves obrigatórias em sua definição
    """

    # Extraindo chaves do dicionário
    data_dict_keys = [list(data_dict[t].keys()) for t in data_dict.keys()]

    # Iterando sobre lista de listas e validando
    for keys in data_dict_keys:
        assert all(key in keys for key in required_data_dict_keys)
