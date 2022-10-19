"""
MÓDULO: terraglue.py

CONTEXTO:
---------
Módulo terraglue criado para consolidar classes, métodos,
atributos, funções e implementações no geral que possam
facilitar a construção de jobs Glue utilizando a linguagem
Python como principal ferramenta. Neste módulo, será
possível encontrar uma série de funcionalidades criadas
a partir de experimentações práticas envolvendo o
levantamento das principais dificuldades e da aplicação
de boas práticas de desenvolvimento de aplicações Spark.

OBJETIVO:
---------
Consolidar elementos responsáveis por auxiliar e acelearar
o desenvolvimento de aplicações Spark a serem utilizadas
como jobs do Glue.

TABLE OF CONTENTS:
------------------
1. Preparação inicial do script
    1.1 Importação das bibliotecas
    1.2 Configuração do objeto logger
    1.3 Definição de variáveis do módulo
2. Gerenciamento de jobs
3. Gerenciamento de transformações
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Bibliotecas utilizadas na construção do módulo
import sys
import logging
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
        1.3 Definindo variáveis da aplicação
---------------------------------------------------"""

# Variáveis de controle das classes
VERBOSE = -1


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
log_date_format = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(log_format,
                              datefmt=log_date_format)

# Configurando stream handler do objeto de log
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


"""---------------------------------------------------
-------------- 2. GERENCIAMENTO DE JOBS --------------
            2.1 Definição de classe Python
---------------------------------------------------"""


class GlueJobManager():
    """
    """

    def __init__(self,
                 argv_list: list,
                 output_bucket: str,
                 output_db: str,
                 output_table: str,
                 connection_type: str,
                 update_behavior: str,
                 partition_keys: list,
                 compression: str,
                 enable_update_catalog: bool,
                 verbose=VERBOSE) -> None:

        self.argv_list = argv_list
        self.output_bucket = output_bucket
        self.output_db = output_db
        self.output_table = output_table
        self.connection_type = connection_type
        self.update_behavior = update_behavior
        self.partition_keys = partition_keys
        self.compression = compression
        self.enable_update_catalog = enable_update_catalog
        self.verbose = verbose

    # Obtendo argumentos do job
    def get_args(self) -> None:
        logger.info(f"Obtendo argumentos do job ({self.argv_list})")
        try:
            self.job_args = getResolvedOptions(sys.argv, self.argv_list)
        except Exception as e:
            logger.error("Erro ao retornar argumentos do job dentro da " +
                         f"lista informada. Exception: {e}")
            raise e

    # Obtendo elementos de contexto e sessão da aplicação
    def get_context_and_session(self) -> None:
        logger.info("Criando SparkContext, GlueContext e SparkSession")
        try:
            self.sc = SparkContext()
            self.glueContext = GlueContext(self.sc)
            self.spark = self.glueContext.spark_session
        except Exception as e:
            logger.error("Erro ao criar elementos de contexto e sessão " +
                         f"da aplicação. Exception: {e}")
            raise e

    # Inicializando objeto de job a partir de contexto do Glue
    def init_job(self):
        # Obtendo argumentos e objetos de sessão
        self.get_args
        self.get_context_and_session

        logger.info("Inicializando job a partir de GlueContext")
        try:
            job = Job(self.glueContext)
            job.init(self.args['JOB_NAME'], self.args)
            return job
        except Exception as e:
            logger.error(f"Erro ao inicializar job do Glue. Exception: {e}")
            raise e
