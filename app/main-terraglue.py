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
from datetime import datetime
import sys
import logging
from time import sleep
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, avg, sum,\
    round, countDistinct, max, lit


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
PARTITION_FORMAT = "%Y%m%d_%H%M%S"
PARTITION_VALUE = datetime.now().strftime(PARTITION_FORMAT)

# Variáveis de escrita da tabela final
OUTPUT_BUCKET = "terraglue-sot-data-325483233520-us-east-1" # Automatizar via envio de argumentos pelo Terraform
OUTPUT_DB = "ra8"
OUTPUT_TABLE = "tbsot_ecommerce_br"
OUTPUT_PATH = f"s3://{OUTPUT_BUCKET}/{OUTPUT_DB}/{OUTPUT_TABLE}"
CONNECTION_TYPE = "s3"
UPDATE_BEHAVIOR = "UPDATE_IN_DATABASE"
PARTITION_KEYS = [PARTITION_NAME]
DATA_FORMAT = "glueparquet"
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
    },
    "payments": {
        "database": "ra8",
        "table_name": "payments",
        "transformation_ctx": "dyf_payments"
    },
    "reviews": {
        "database": "ra8",
        "table_name": "reviews",
        "transformation_ctx": "dyf_reviews"
    }
}


"""---------------------------------------------------
-------------- 2. GERENCIAMENTO DE JOBS --------------
            2.1 Definição de classe Python
---------------------------------------------------"""


class GlueJobManager():
    """
    """

    def __init__(self, argv_list: list) -> None:

        self.argv_list = argv_list

    # Obtendo argumentos do job
    def get_args(self) -> None:
        logger.info(f"Obtendo argumentos do job ({self.argv_list})")
        try:
            self.args = getResolvedOptions(sys.argv, self.argv_list)
        except Exception as e:
            logger.error("Erro ao retornar argumentos do job dentro da "
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
            logger.error("Erro ao criar elementos de contexto e sessão "
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


"""---------------------------------------------------
--------- 2. GERENCIAMENTO DE TRANSFORMAÇÕES ---------
            2.2 Definição de classe Python
---------------------------------------------------"""


class GlueTransformationManager(GlueJobManager):
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
                 data_format: str,
                 partition_keys: list,
                 compression: str,
                 enable_update_catalog: bool) -> None:

        self.argv_list = argv_list
        self.data_dict = data_dict
        self.output_bucket = output_bucket
        self.output_db = output_db
        self.output_table = output_table
        self.output_path = f"s3://{self.output_bucket}" \
            f"/{self.output_db}/{self.output_table}"
        self.connection_type = connection_type
        self.update_behavior = update_behavior
        self.data_format = data_format
        self.partition_keys = partition_keys
        self.compression = compression
        self.enable_update_catalog = enable_update_catalog

        # Herdando atributos de classe de gerenciamento de job
        GlueJobManager.__init__(self, argv_list=self.argv_list)

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
        sleep(0.01)
        try:
            # Criando dicionário de Dynamic Frames
            dynamic_dict = {k: dyf for k, dyf
                            in zip(self.data_dict.keys(), dynamic_frames)}
            logger.info("Dados gerados com sucesso. Total de DynamicFrames: " +
                        f"{len(dynamic_dict.values())}")
        except Exception as e:
            logger.error("Erro ao mapear DynamicFrames às chaves do "
                         f"dicionário de dados fornecido. Exception: {e}")
            raise e

        # Retornando dicionário de DynamicFrames
        sleep(0.01)
        return dynamic_dict

    # Gerando dicionário de DataFrames Spark do projeto
    def generate_dataframes_dict(self) -> dict:
        # Gerando dicionário de DynamicFrames
        dyf_dict = self.generate_dynamic_frames_dict()

        # Transformando DynamicFrames em DataFrames
        logger.info(f"Transformando os {len(dyf_dict.keys())} "
                    "DynamicFrames em DataFrames Spark")
        try:
            df_dict = {k: dyf.toDF() for k, dyf in dyf_dict.items()}
            logger.info("DataFrames Spark gerados com sucesso")
        except Exception as e:
            logger.error("Erro ao transformar DynamicFrames em "
                         f"DataFrames Spark. Exception: {e}")
            raise e

        # Retornando dicionário de DataFrames Spark convertidos
        sleep(0.01)
        return df_dict

    # Método de transformação: payments
    @staticmethod
    def transform_payments(df: DataFrame) -> DataFrame:
        """
        """

        logger.info("Preparando DAG de transformações para a base df_payments")
        try:
            # Retornando o tipo de pagamento mais comum para cada pedido
            df_most_common_payments = df.groupBy("order_id", "payment_type")\
                .count()\
                .sort(col("count").desc(), "payment_type")\
                .dropDuplicates(["order_id"])\
                .withColumnRenamed("payment_type", "most_common_payment_type")\
                .drop("count")

            # Preparando base de pagamentos para extração de alguns atributos
            df_payments_aggreg = df.groupBy("order_id").agg(
                count("order_id").alias("installments"),
                round(sum("payment_value"), 2).alias("sum_payments"),
                round(avg("payment_value"), 2).alias("avg_payment_value"),
                countDistinct("payment_type").alias("distinct_payment_types")
            )

            # Enriquecendo base de pagamentos com tipo de pagamento mais comum
            df_payments_join = df_payments_aggreg.join(
                other=df_most_common_payments,
                on=[df_payments_aggreg.order_id ==
                    df_most_common_payments.order_id],
                how="left"
            ).drop(df_most_common_payments.order_id)

            # Alterando ordem das colunas
            df_payments_prep = df_payments_join.select(
                "order_id",
                "installments",
                "sum_payments",
                "avg_payment_value",
                "distinct_payment_types",
                "most_common_payment_type"
            )

            # Retornando DataFrame preparado
            return df_payments_prep
        except Exception as e:
            logger.error("Erro ao preparar DAG de transformações para dados "
                         f"de pagamentos. Exception: {e}")
            raise e

    # Método de transformação: reviews
    @staticmethod
    def transform_reviews(df: DataFrame) -> DataFrame:
        """
        """

        logger.info("Preparando DAG de transformações para a base df_reviews")
        try:
            # Aplicando filtros iniciais para eliminar ruídos na tabela
            df_reviews_filtered = df\
                .where("order_id is not null")\
                .where("length(review_score) = 1")

            # Coletando nota máxima por pedido
            df_reviews_prep = df_reviews_filtered.select(
                col("order_id"),
                col("review_score").cast("int"),
                col("review_comment_message")
            ).groupBy("order_id").agg(
                max("review_score").alias("review_best_score"),
                max("review_comment_message").alias("review_comment_message")
            ).drop_duplicates(["order_id"])

            # Retornando DataFrame
            return df_reviews_prep
        except Exception as e:
            logger.error("Erro ao preparar DAG de transformações "
                         f"de reviews de pedidos. Exception: {e}")
            raise e

    # Método de transformação: tabela final
    @staticmethod
    def transform_sot(**kwargs) -> DataFrame:
        """
        """

        # Desempacotando DataFrames dos argumentos da função
        df_orders_prep = kwargs["df_orders_prep"]
        df_customers_prep = kwargs["df_customers_prep"]
        df_payments_prep = kwargs["df_payments_prep"]
        df_reviews_prep = kwargs["df_reviews_prep"]

        # Gerando base final com atributos enriquecidos
        logger.info("Preparando DAG para geração de tabela final enriquecida")
        try:
            df_sot_prep = df_orders_prep.join(
                other=df_customers_prep,
                on=[df_orders_prep.customer_id ==
                    df_customers_prep.customer_id],
                how="left"
            ).drop(df_customers_prep.customer_id).join(
                other=df_payments_prep,
                on=[df_orders_prep.order_id == df_payments_prep.order_id],
                how="left"
            ).drop(df_payments_prep.order_id).join(
                other=df_reviews_prep,
                on=[df_orders_prep.order_id == df_reviews_prep.order_id],
                how="left"
            ).drop(df_reviews_prep.order_id)
        except Exception as e:
            logger.error("Erro ao preparar DAG para tabela final. "
                         f"Exception: {e}")
            raise e

        # Retornando base final
        return df_sot_prep

    # Método de transformação: adição de partição
    @staticmethod
    def add_partition(df: DataFrame,
                      partition_name: str,
                      partition_value) -> DataFrame:
        """
        """

        logger.info("Adicionando partição na tabela "
                    f"({partition_name}={partition_value})")
        try:
            df_partitioned = df.withColumn(partition_name,
                                           lit(partition_value))
        except Exception as e:
            logger.error("Erro ao adicionar coluna de partição ao DataFrame "
                         f"via método .withColumn(). Exception: {e}")

        # Retornando DataFrame com coluna de partição
        return df_partitioned

    # Escrevendo e catalogando resultado final
    def write_data_to_catalog(self, df: DataFrame or DynamicFrame) -> None:
        """
        """

        # Convertendo DataFrame em DynamicFrame
        if type(df) == DataFrame:
            logger.info("Transformando DataFrame preparado em DynamicFrame")
            try:
                dyf = DynamicFrame.fromDF(df, self.glueContext, "dyf")
            except Exception as e:
                logger.error("Erro ao transformar DataFrame em DynamicFrame. "
                             f"Exception: {e}")
                raise e
        else:
            dyf = df

        # Criando sincronização com bucket s3
        logger.info("Preparando e sincronizando elementos de saída da tabela")
        try:
            data_sink = self.glueContext.getSink(
                path=self.output_path,
                connection_type=self.connection_type,
                updateBehavior=self.update_behavior,
                partitionKeys=self.partition_keys,
                compression=self.compression,
                enableUpdateCatalog=self.enable_update_catalog,
                transformation_ctx="data_sink",
            )
        except Exception as e:
            logger.error("Erro ao configurar elementos de saída via getSink. "
                         f"Exception: {e}")
            raise e

        # Configurando informações do catálogo de dados
        logger.info("Adicionando entrada para tabela no catálogo de dados")
        try:
            data_sink.setCatalogInfo(
                catalogDatabase=self.output_db,
                catalogTableName=self.output_table
            )
            data_sink.setFormat(self.data_format)
            data_sink.writeFrame(dyf)

            logger.info(f"Tabela {self.output_db}.{self.output_table} "
                        "atualizada com sucesso no catálogo. Seus dados estão "
                        f"armazenados em {self.output_path}")
        except Exception as e:
            logger.error("Erro ao adicionar entrada para tabela no catálogo "
                         f"de dados. Exception: {e}")
            raise e

    # Encapsulando método único para execução do job
    def run(self) -> None:
        """
        """

        # Preparando insumos do job
        job = self.init_job()

        # Lendo DynamicFrames e transformando em DataFrames Spark
        dfs_dict = self.generate_dataframes_dict()

        # Separando DataFrames em variáveis
        df_orders = dfs_dict["orders"]
        df_customers = dfs_dict["customers"]
        df_payments = dfs_dict["payments"]
        df_reviews = dfs_dict["reviews"]

        # Transformando dados
        df_payments_prep = self.transform_payments(df=df_payments)
        df_reviews_prep = self.transform_reviews(df=df_reviews)

        # Gerando base final com atributos enriquecidos
        df_sot_prep = self.transform_sot(
            df_orders_prep=df_orders,
            df_customers_prep=df_customers,
            df_payments_prep=df_payments_prep,
            df_reviews_prep=df_reviews_prep
        )

        # Adicionando partição ao DataFrame
        df_sot_prep_partitioned = self.add_partition(
            df=df_sot_prep,
            partition_name=PARTITION_NAME,
            partition_value=PARTITION_VALUE
        )

        # Escrevendo e catalogando dados
        self.write_data_to_catalog(df=df_sot_prep_partitioned)

        # Commitando job
        job.commit()


"""---------------------------------------------------
--------------- 4. PROGRAMA PRINCIPAL ----------------
         Execução do job a partir de classes
---------------------------------------------------"""

if __name__ == "__main__":

    # Inicializando objeto para gerenciar o job e as transformações
    glue_manager = GlueTransformationManager(
        argv_list=ARGV_LIST,
        data_dict=DATA_DICT,
        output_bucket=OUTPUT_BUCKET,
        output_db=OUTPUT_DB,
        output_table=OUTPUT_TABLE,
        connection_type=CONNECTION_TYPE,
        update_behavior=UPDATE_BEHAVIOR,
        data_format=DATA_FORMAT,
        partition_keys=PARTITION_KEYS,
        compression=COMPRESSION,
        enable_update_catalog=ENABLE_UPDATE_CATALOG
    )

    # Executando todas as lógicas mapeadas do job
    glue_manager.run()


# Inserir argumentos do job direto via terraform
# Printar argumentos do job como mensagem de log no início do projeto (--JOB_NAME=X --OUTPUT_BUCKET=1)
