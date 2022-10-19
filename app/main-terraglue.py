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
4. Programa principal
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
          1.2 Configuração do objeto logger
---------------------------------------------------"""

# Instanciando objeto de logging
logger = logging.getLogger("glue_logger")
logger.setLevel(logging.INFO)

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
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
        1.3 Definindo variáveis da aplicação
---------------------------------------------------"""

# Argumentos do job
ARGV_LIST = ['JOB_NAME']

# Definindo partição
PARTITION_NAME = "anomesdia_hms"
PARTITION_FORMAT = "yyyyMMdd_HHmmss"

# Variáveis de escrita da tabela final
OUTPUT_BUCKET = "aws-sot-data-739870437205-us-east-1"
OUTPUT_DB = "ra8"
OUTPUT_TABLE = "tbsot_ecommerce_br"
OUTPUT_PATH = f"s3://{OUTPUT_BUCKET}/{OUTPUT_DB}/{OUTPUT_TABLE}"
CONNECTION_TYPE = "s3"
UPDATE_BEHAVIOR = "UPDATE_IN_DATABASE"
PARTITION_KEYS = [PARTITION_NAME]
COMPRESSION = "snappy"
ENABLE_UPDATE_CATALOG = True

# Variáveis de controle das classes
VERBOSE = -1

# Definindo dicionário para mapeamento dos dados
DATA_DICT = {
    "orders": {
        "database": "ra8",
        "table_name": "orders",
        "transformation_ctx": "dyf_orders",
    },
    "customers": {
        "database": "ra8",
        "table_name": "customers",
        "transformation_ctx": "dyf_customers"
    }
}


"""---------------------------------------------------
-------------- 2. GERENCIAMENTO DE JOBS --------------
            2.1 Definição de classe Python
---------------------------------------------------"""


class GlueJobManager():
    """
    """

    def __init__(self,
                 argv_list: list,
                 data_dict: dict,
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
        self.data_dict = data_dict
        self.output_bucket = output_bucket
        self.output_db = output_db
        self.output_table = output_table
        self.output_path = f"s3://{self.output_bucket}" \
            f"/{self.output_db}/{self.output_table}"
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
            self.args = getResolvedOptions(sys.argv, self.argv_list)
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
    def init_job(self) -> Job:
        # Obtendo argumentos e objetos de sessão
        self.get_args()
        self.get_context_and_session()

        print(self.sc)
        print(self.glueContext)
        print(self.spark)

        logger.info("Inicializando job a partir de GlueContext")
        try:
            job = Job(self.glueContext)
            job.init(self.args['JOB_NAME'], self.args)
            return job
        except Exception as e:
            logger.error(f"Erro ao inicializar job do Glue. Exception: {e}")
            raise e

    # Gerando dicionário de DynamicFrames do projeto
    def generate_dynamic_frames_dict(self) -> dict:
        logger.info("Iterando sobre dicionário de dados fornecido para " +
                    "leitura de DynamicFrames do Glue")
        try:
            # Lendo DynamicFrames e salvando em lista
            dynamic_frames = [
                self.glueContext.create_dynamic_frame.from_catalog(
                    database=self.data_dict[t]["database"],
                    table_name=self.data_dict[t]["table_name"],
                    transformation_ctx=self.data_dict[t]["transformation_ctx"]
                ) for t in self.data_dict.keys()
            ]
        except Exception as e:
            logger.error("Erro ao gerar lista de DynamicFrames com base " +
                         f"em dicionário. Exception: {e}")
            raise e

        logger.info("Mapeando DynamicFrames às chaves do dicionário")
        try:
            # Criando dicionário de Dynamic Frames
            dynamic_dict = {k: type(dyf) for k, dyf
                            in zip(self.data_dict.keys(), dynamic_frames)}
            logger.info("Dados gerados com sucesso. Total de DynamicFrames: " +
                        f"{len(dynamic_dict.values())}")
            return dynamic_dict
        except Exception as e:
            logger.error("Erro ao mapear DynamicFrames às chaves do "
                         f"dicionário de dados fornecido. Exception: {e}")
            raise e

    # Gerando dicionário de DataFrames Spark do projeto
    def generate_dataframes_dict(self) -> dict:
        # Gerando dicionário de DynamicFrames
        dyf_dict = self.generate_dynamic_frames_dict()

        # Transformando DynamicFrames em DataFrames
        logger.info(f"Transformando os {len(dyf_dict.keys())} " +
                    "DynamicFrames em DataFrames Spark")
        try:
            return {k: type(dyf) for k, dyf in dyf_dict.items()}
        except Exception as e:
            logger.error("Erro ao transformar DynamicFrames em "
                         f"DataFrames Spark. Exception: {e}")
            raise e


"""---------------------------------------------------
--------- 2. GERENCIAMENTO DE TRANSFORMAÇÕES ---------
            2.2 Definição de classe Python
---------------------------------------------------"""


class GlueTransformationManager(GlueJobManager):
    """
    """

    def __init__(self, data_dict: dict) -> None:
        self.data_dict = data_dict


"""---------------------------------------------------
--------------- 4. PROGRAMA PRINCIPAL ----------------
         Execução do job a partir de classes
---------------------------------------------------"""

if __name__ == "__main__":
    # Inicializando objeto da classe de gerenciamento do job
    job_manager = GlueJobManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT,
        output_bucket=OUTPUT_BUCKET,
        output_db=OUTPUT_DB,
        output_table=OUTPUT_TABLE,
        connection_type=CONNECTION_TYPE,
        update_behavior=UPDATE_BEHAVIOR,
        partition_keys=PARTITION_KEYS,
        compression=COMPRESSION,
        enable_update_catalog=ENABLE_UPDATE_CATALOG,
        verbose=VERBOSE
    )

    # Inicializando objeto para gerenciar transformações do job
    transformation_manager = GlueTransformationManager(
        data_dict=DATA_DICT
    )

    # Preparando insumos do job
    job = job_manager.init_job()

    # Coletando DynamicFrames
    dyf_dict = job_manager.generate_dynamic_frames_dict()
    df_orders = dyf_dict["orders"].toDF()
    df_orders.show(5)

"""Todo
- [] Avaliar se a classe GlueJobManager realmente precisa de todos esses argumentos relacionados à saída dos dados
- [] Avaliar se a classe GlueTransformationManager era quem deveria receber tais argumentos
- [] Avaliar se a classe GlueTransformationManager deve receber os métodos de leitura dos dados
- [] Avaliar como cumprir a herança entre as classes
- [] Investigar pq não tá sendo possível converter dyfs em dfs
"""


# class GlueTransformationManager
# def transform_assunto_especifico(df : DataFrame) -> DataFrame
# def transform_assunto_especifico(df : DataFrame) -> DataFrame
# def transform_assunto_especifico(df : DataFrame) -> DataFrame
# def run():
#       df1 = transform_assunto_especifico(df)
#       df2 = transform_assunto_especifico(df)
#       df3 = transform_assunto_especifico(df)
#       return df