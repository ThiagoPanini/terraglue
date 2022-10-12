"""
MÓDULO: src.local.py

CONTEXTO:
---------
Módulo criado para centralizar as operações necessárias
para a realização da leitura local de arquivos dentro
de uma aplicação Spark.

OBJETIVO:
---------
Consolidar e organizar funções responsáveis por ler
fontes de dados externas e disponibilizar os resultados
como DataFrames do Spark

TABLE OF CONTENTS:
------------------
1. Preparação inicial do script
    1.1 Importação das bibliotecas
    1.2 Configuração do objeto logger
    1.3 Definição de variáveis da aplicação
2. Funções para leitura de arquivos

------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Bibliotecas do módulo
import os
import logging


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
        1.3 Definindo variáveis da aplicação
---------------------------------------------------"""

# Definindo variávies para leitura dos arquivos
DATA_PATH = "data/"
FILE_FORMAT = "csv"


# Consolidando etapas para leitura local
def read_local_data(spark, data_path=DATA_PATH) -> list:
    """
    """

    # Caminhos de arquivos existentes no diretório alvo
    try:
        logger.info("Obtendo caminhos de arquivos no diretório alvo")
        files_path = [os.path.join(dirs, files[0])
                      for dirs, _, files in os.walk(data_path)
                      if files != []]
    except Exception as e:
        logger.error(f"Erro ao obter caminhos de arquivos. Exception: {e}")
        raise e

    # Iterando sobre cada arquivo e obtendo DataFrame
    try:
        logger.debug("Realizando a leitura dos arquivos encontrados")
        dfs = [
            spark.read.format("csv").option("header", "true")
                                    .option("inferSchema", "true")
                                    .load(p) for p in files_path
        ]
        logger.info(f"Leitura realizada com sucesso de {len(dfs)} " +
                    "DataFrames Spark")
    except Exception as e:
        logger.error(f"Erro ao realizar a leitura dos arquivos. Exception {e}")

    return dfs
