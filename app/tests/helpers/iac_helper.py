"""
MÓDULO: iac_helper.py

CONTEXTO:
---------
Módulo criado para facilitar algumas operações integradas
aos códigos declarados no Terraform para facilitar a
construção dos testes unitários da aplicação.


OBJETIVO:
---------
Proporcionar uma série de funcionalidades capazes de
facilitar a construção de testes unitários em situações
que envolvem a extração de informações presentes nos
arquivos terraform.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Bibliotecas utilizadas no módulo
import os


# Definindo variáveis de diretório
PATH_INFRA = os.path.join(os.getcwd(), "infra")
PATH_VAR_TF = os.path.join(PATH_INFRA, "variables.tf")


"""---------------------------------------------------
------- 2. EXTRAÇÃO DE CONTEÚDO DE ARQUIVOS TF -------
              2.1 Gerando dados ficítios
---------------------------------------------------"""


# Extraindo conteúdo de variáveis Terraform do tipo map
def extract_map_variable_from_ferraform(var_name: str,
                                        variables_tf_path=PATH_VAR_TF) -> dict:
    """
    Realiza a extração do conteúdo de uma variável Terraform do
    tipo map declarada em arquivo de variables.tf com base em um
    nome de referência. A extração da informação é feita através
    da leitura do arquivo de variáveis e subsequente iterações
    responsáveis por identificar índices onde o nome da variável
    aparece e, dessa forma, aplicar subsequentes processos de
    preparação de strings para obter o conteúdo da variável do
    tipo map em um dicionário Python.

    Parâmetros
    ----------
    :param variables_tf_path:
        Caminho onde o arquivo de variáveis do Terraform está
        armazenado.
        [type: string, default=PATH_VAR_TF]

    :param var_name:
        Nome de referência da variável do tipo map a ter seu
        conteúdo extraído e transformado em um dicionário
        Python para posterior análise. O nome da variável
        passado neste argumento deve ser idêntico ao nome
        declarado para a mesma variável no arquivo Terraform.
        [type: string]

    Retorno
    -------
    :return map_dict:
        Dicionário Python contendo as informações extraídas da
        variável Terraform declarada no arquivo em questão.
        [type: dict]
    """

    # Lendo arquivo de variáveis do terraform
    with open(variables_tf_path, "r") as f:
        file = f.readlines()

    # Coletando início da lista onde a variável desejada aparece
    line_var = [lv for lv in file if var_name in lv]
    idx_var = file.index(line_var[0])

    # Coletando índice da próxima variável declara para slice
    line_next_var = [lnv for lnv in file[idx_var + 1:] if "variable" in lnv]
    idx_next_var = file.index(line_next_var[0])

    # Aplicando slice na lista para coleta de variável
    var_list = file[idx_var:idx_next_var]

    # Coletando início da declaração do map
    line_map = [lm for lm in var_list if "default" in lm]
    idx_map = var_list.index(line_map[0])

    # Coletando final da declaração do map para slice
    line_end_map = [lem for lem in var_list[idx_map:] if "}" in lem]
    idx_end_map = var_list.index(line_end_map[0])

    # Aplicando slice para coleta de map definido para a variável
    map_list = var_list[idx_map + 1:idx_end_map]
    map_list_prep = [
        m.strip()
        .replace('"', '')
        .replace('--', '')
        .replace('\n', '')
        for m in map_list
    ]

    # Transformando em dicionário
    map_dict = {
        arg.strip(): value.strip() for v in map_list_prep
        for arg, value in zip([v.split("=")[0]], [v.split("=")[1]])
    }

    return map_dict
