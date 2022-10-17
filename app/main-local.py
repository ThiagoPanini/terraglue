"""
SCRIPT: main.py

CONTEXTO:
---------
Script criado para servir como uma aplicação Spark
implantada através do serviço AWS Glue para leitura e
processamento de dados relacionados ao e-commerce
brasileiro.

OBJETIVO:
---------
Consolidar múltiplas fontes externas de dados contendo
informações sobre compras e atividades no cenário do
e-commerce brasileiro registrado pela empresa Olist,
permitindo assim a construção de um dataset completo,
não normalizado e com atributos suficientemente ricos
de modo a garantir análises eficientes em outras etapas
do fluxo analítico.

TABLE OF CONTENTS:
------------------
1. Preparação inicial do script
    1.1 Importação das bibliotecas
    1.2 Configuração do objeto logger
    1.3 Definição de variáveis da aplicação
2. Transformações na aplicação Spark
    2.1 Lendo dados e obtendo DataFrames
    2.2 Preparando dados de pagamentos
    2.3 Preparando dados de reviews de pedidos
    2.4 Gerando base final a partir de joins

------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Bibliotecas da aplicação
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg,\
    sum, round, count_distinct, max
from src.local import read_local_data
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

# Criando sessão Spark
logger.debug("Criando e obtendo objeto de sessão Spark")
try:
    spark = SparkSession\
        .builder\
        .appName("ecommerce-data-processing")\
        .getOrCreate()
except Exception as e:
    logger.error(f"Erro ao obter objeto de sessão Spark. Exception: {e}")


"""---------------------------------------------------
-------- 2. TRANSFORMAÇÕES NA APLICAÇÃO SPARK --------
          2.1 Lendo dados e obtendo DataFrames
---------------------------------------------------"""

# Obtendo DataFrames a serem utilizados
df_orders, df_reviews,\
    df_payments, df_customers, _ = read_local_data(spark=spark)


"""---------------------------------------------------
-------- 2. TRANSFORMAÇÕES NA APLICAÇÃO SPARK --------
          2.2 Preparando dados de pagamentos
---------------------------------------------------"""

logger.info("Preparando DAG de transformações para dados de pagamentos")
try:
    # Retornando o tipo de pagamento mais comum para cada pedido
    df_most_common_payments = df_payments.groupBy("order_id", "payment_type")\
        .count()\
        .sort(col("count").desc(), "payment_type")\
        .dropDuplicates(["order_id"])\
        .withColumnRenamed("payment_type", "most_common_payment_type")\
        .drop("count")

    # Preparando base de pagamentos para extração de alguns atributos
    df_payments_aggreg = df_payments.groupBy("order_id").agg(
        count("order_id").alias("installments"),
        round(sum("payment_value"), 2).alias("sum_payments"),
        round(avg("payment_value"), 2).alias("avg_payment_value"),
        count_distinct("payment_type").alias("distinct_payment_types")
    )

    # Enriquecendo base de pagamentos com tipo de pagamento mais comum
    df_payments_join = df_payments_aggreg.join(
        other=df_most_common_payments,
        on=[df_payments_aggreg.order_id == df_most_common_payments.order_id],
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
except Exception as e:
    logger.error("Erro ao preparar DAG de transformações para dados " +
                 f"de pagamentos. Exception: {e}")


"""---------------------------------------------------
-------- 2. TRANSFORMAÇÕES NA APLICAÇÃO SPARK --------
      2.3 Preparando dados de reviews de pedidos
---------------------------------------------------"""

logger.info("Preparando DAG de transformações para reviews de pedidos")
try:
    # Aplicando filtros iniciais para eliminar ruídos na tabela
    df_reviews_filtered = df_reviews\
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
except Exception as e:
    logger.error("Erro ao preparar DAG de transformações " +
                 f"de reviews de pedidos. Exception: {e}")


"""---------------------------------------------------
-------- 2. TRANSFORMAÇÕES NA APLICAÇÃO SPARK --------
      2.4 Gerando base final a partir de joins
---------------------------------------------------"""

logger.info("Preparando DAG para geração de tabela final enriquecida")
try:
    # Gerando base final com atributos enriquecidos
    df_sot_ecommerce = df_orders.join(
        other=df_customers,
        on=[df_orders.customer_id == df_customers.customer_id],
        how="left"
    ).drop(df_customers.customer_id).join(
        other=df_payments_prep,
        on=[df_orders.order_id == df_payments_prep.order_id],
        how="left"
    ).drop(df_payments_prep.order_id).join(
        other=df_reviews_prep,
        on=[df_orders.order_id == df_reviews_prep.order_id],
        how="left"
    ).drop(df_reviews_prep.order_id)
except Exception as e:
    logger.error(f"Erro ao preparar DAG para tabela final. Exception: {e}")

