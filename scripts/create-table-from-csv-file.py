"""
SCRIPT: brazilian-ecommerce.py

CONTEXTO:
---------
Script criado para automatizar a geração de comandos de
criação de tabelas com base em diretório local de arquivos
organizando de maneira a simular o armazenamento de tabelas
em bucket s3 na AWS. Os comandos gerados por este script
poderão ser utilizados no contexto de criação de entradas
no catálogo de dados do Glue em uma conta AWS para a
posterior leitura através de jobs do próprio Glue.

OBJETIVO:
---------
Gerar múltiplos arquivos .sql (ou .txt) contendo comandos
de criação de tabelas com base no conteúdo presente nos
arquivos físicos armazenados localmente.

TABLE OF CONTENTS:
------------------
1. Preparação inicial do script
    1.1 Importação das bibliotecas
    1.2 Configuração do objeto logger
    1.3 Coleta e validação dos argumentos
2. Programa principal
    2.1 Criando e configurando SparkSession
    2.2 Lendo objetos do s3 em DataFrames Spark
    2.3 Cruzando e preparando dados
    2.4 Criando coluna de partição da tabela
    2.5 Escrevendo tabela final em bucket no s3

------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Importando bibliotecas
import sys
import argparse
import logging
import os


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.2 Configuração do objeto logger
---------------------------------------------------"""

# Instanciando objeto de logging
logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)

# Configurando formato das mensagens no objeto
log_format = "%(levelname)s;%(asctime)s;%(filename)s;"
log_format += "%(lineno)d;%(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(log_format,
                              datefmt=date_format)

# Configurando stream handler do objeto de log
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
        1.3 Definição e coleta dos argumentos
---------------------------------------------------"""

# Criando objeto para parse dos argumentos
parser = argparse.ArgumentParser(
    prog=sys.argv[0],
    usage=f"python3 {__file__} <data_path>",
    description="Script criado para automatizar a geração de comandos de " +
                "criação de tabelas com base em diretório local de arquivos "
                "organizando de maneira a simular o armazenamento de tabelas "
                "em bucket s3 na AWS."
)

# Adicionando argumento: --version
parser.add_argument(
    "-v", "--version",
    action="version",
    version=f"{os.path.splitext(parser.prog)[0]} 0.1"
)

# Adicionando argumento: --data-path
parser.add_argument(
    "-d", "--data-path",
    dest="data_path",
    type=str,
    default="./data",
    help="Diretório local de armazenamento dos arquivos de origem",
    required=False
)

# Adicionando argumento: --command-format
parser.add_argument(
    "-cf", "--command-format",
    dest="command_format",
    type=str,
    default="sql",
    choices=["sql", "txt"],
    help="Extensão do arquivo gerado com o comando de criação de tabela",
    required=False
)

# Adicionando argumento: --output-path
parser.add_argument(
    "-o", "--output-path",
    dest="output_path",
    type=str,
    default="./infra/modules/analytics/create-table",
    help="Diretório para salvamento dos comandos de criação de tabela",
    required=False
)

# Coletando argumentos do script
args = parser.parse_args()


if __name__ == "__main__":

    """-----------------------------------------------
    ------------- 2. PROGRAMA PRINCIPAL --------------
          2.1 Gerando listas com informações locais
    -----------------------------------------------"""

    # Iterando sobre diretório de dados e extraindo informações relevantes
    files_path = [os.path.join(dirs, files[0])
                  for dirs, _, files in os.walk(args.data_path) if files != []]
    glue_databases = [p.removeprefix(args.data_path)[1:]
                      .split("/")[0] for p in files_path]
    table_names = [p.removeprefix(args.data_path)[1:]
                   .split("/")[1].replace('-', '_') for p in files_path]

    """-----------------------------------------------
    ------------- 2. PROGRAMA PRINCIPAL --------------
       2.2 Gerando e salvando comandos CREATE TABLE
    -----------------------------------------------"""

    # Iterando sobre informações dos arquivos
    for db, tbl, path in zip(glue_databases, table_names, files_path):
        # Realizando leitura de arquivo e coletando header
        with open(path, "r") as raw:
            header = raw.readline()

        # Preparando header e gerando lista de colunas
        header_prep = header.replace("\n", "").replace('"', "").split(',')
        columns = ',\n'.join(["\t" + h.lower() + " STRING"
                              for h in header_prep])

        # Gerando comando de criação de tabelas
        create_table = f'CREATE EXTERNAL TABLE {db}.{tbl} (\n{columns}\n)' \
            + '\nCOMMENT "Tabela criada para fins de validação e testes"' \
            + '\nROW FORMAT DELIMITED' \
            + '\n\tFIELDS TERMINATED BY ","' \
            + '\n\tLINES TERMINATED BY "\\n"' \
            + '\nSTORED AS TEXTFILE' \
            + f'\nLOCATION "s3://<bucket_name>/{db}/{tbl}"' \
            + '\nTBLPROPERTIES ("skip.header.line.count"="1")'

        # Salvando comandos em arquivos locais
        command_filename = f"{db}_{tbl}.{args.command_format}"
        output_command_path = os.path.join(args.output_path, command_filename)
        with open(output_command_path, "w") as c:
            c.write(create_table)
