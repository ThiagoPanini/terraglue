"""
JOB: main.py

CONTEXTO:
---------
Script principal da aplicação Spark implantada como job do
Glue dentro dos contextos estabelecidos pelo processo de
ETL a ser programado.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Bibliotecas utilizadas na construção do módulo
from datetime import datetime
from pyspark.sql import DataFrame
from pyspark.sql.functions import col, count, avg, sum,\
    round, countDistinct, max, expr
from terraglue import GlueETLManager, log_config


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
        1.2 Definindo variáveis da aplicação
---------------------------------------------------"""

# Configurando objeto de log
logger = log_config(logger_name=__file__)

# Argumentos do job
ARGV_LIST = [
    "JOB_NAME",
    "OUTPUT_BUCKET",
    "OUTPUT_DB",
    "OUTPUT_TABLE",
    "CONNECTION_TYPE",
    "UPDATE_BEHAVIOR",
    "PARTITION_NAME",
    "PARTITION_FORMAT",
    "DATA_FORMAT",
    "COMPRESSION",
    "ENABLE_UPDATE_CATALOG",
    "NUM_PARTITIONS"
]

# Definindo dicionário para mapeamento dos dados
DATA_DICT = {
    "orders": {
        "database": "ra8",
        "table_name": "orders",
        "transformation_ctx": "dyf_orders",
        "create_temp_view": True
    },
    "order_items": {
        "database": "ra8",
        "table_name": "order_items",
        "transformation_ctx": "dyf_order_items",
        "create_temp_view": True
    },
    "customers": {
        "database": "ra8",
        "table_name": "customers",
        "transformation_ctx": "dyf_customers",
        "create_temp_view": True
    },
    "payments": {
        "database": "ra8",
        "table_name": "payments",
        "transformation_ctx": "dyf_payments",
        "create_temp_view": True
    },
    "reviews": {
        "database": "ra8",
        "table_name": "reviews",
        "transformation_ctx": "dyf_reviews",
        "create_temp_view": True
    }
}


"""---------------------------------------------------
--------- 2. GERENCIAMENTO DE TRANSFORMAÇÕES ---------
            2.2 Definição de classe Python
---------------------------------------------------"""


class GlueTransformationManager(GlueETLManager):
    """
    Classe responsável por gerenciar e fornecer métodos típicos
    de transformação de um job do Glue a serem pontualmente
    adaptados por seus usuários para que as operações nos dados
    possam ser aplicadas de acordo com as necessidades exigidas.

    Em essência, essa classe herda os atributos e métodos da
    classe GlueETLManager existente no módulo terraglue.py,
    permitindo assim o acesso a todos os atributos e métodos
    necessários para inicialização e configuração de um job do Glue.
    Assim, basta que o usuário desenvolva os métodos de
    transformação adequados para seu processo de ETL e coordene
    a execução dos mesmos no método run() desta classe.

    Para maiores informações sobre os atributos, basta consultar
    a documentação das classes e métodos no módulo terraglue.py.
    """

    def __init__(self, argv_list: list, data_dict: dict) -> None:
        self.argv_list = argv_list
        self.data_dict = data_dict

        # Herdando atributos de classe de gerenciamento de job
        GlueETLManager.__init__(self, argv_list=self.argv_list,
                                data_dict=self.data_dict)

    # Método de transformação: orders
    def transform_orders(self, df: DataFrame) -> DataFrame:
        """
        Método de preparação do DataFrame df_orders.
        As etapas de transformação são dadas por:

        1. Conversão dos atributos de data originalmente
           fornecidos como string.
        2. Extração de atributos de data de campo que referencia
           a data de compra do pedido online, permitindo análises
           mais refinidas a respeito da época da compra.

        O método recebe e retorna objetos do tipo DataFrame Spark.
        """

        logger.info("Preparando DAG de transformações para df_orders")
        try:
            # Criando lista de atributos de data para conversão
            date_cols = [
                "order_purchase_timestamp",
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_delivered_customer_date",
                "order_estimated_delivery_date"
            ]

            # Formato de data dos campos da lista
            date_fmt = 'yyyy-MM-dd HH:mm:ss'

            # Iterando sobre campos timestamp e criando novas colunas
            df_orders_date_cast = df
            for c in date_cols:
                df_orders_date_cast = df_orders_date_cast.withColumn(
                    c + "_tmp",
                    expr(f"to_timestamp({c}, '{date_fmt}')")
                ).drop(c)\
                    .withColumnRenamed(c + "_tmp", c)

            # Transformando coluna pontual de data
            df_orders_date_cast = df_orders_date_cast.withColumn(
                "order_estimated_delivery_date",
                expr(f"to_date(order_estimated_delivery_date, '{date_fmt}')")
            )

            # Extraindo atributos de data da compra online
            df_orders_date_prep = self.date_attributes_extraction(
                df=df_orders_date_cast,
                date_col="order_purchase_timestamp",
                convert_string_to_date=False,
                year=True,
                quarter=True,
                month=True,
                dayofmonth=True,
                dayofweek=True,
                dayofyear=True,
                weekofyear=True
            )

            return df_orders_date_prep

        except Exception as e:
            logger.error("Erro ao preparar DAG de transformações para a base "
                         f"df_orders. Exception: {e}")
            raise e

    # Método de transformação: order_items
    def transform_order_items(self, df: DataFrame) -> DataFrame:
        """
        Método de preparação do DataFrame df_orders.
        As etapas de transformação são dadas por:

        1. Extração de agregações e dados estatísticos de pedidos com
        base em itens vendidos por pedido

        O método recebe e retorna objetos do tipo DataFrame Spark.
        """

        logger.info("Preparando DAG de transformações para df_order_items")
        try:
            # Retornando estatísticas de pedidos com base em itens
            df_order_items_stats = df.groupBy("order_id").agg(
                expr("count(1) AS qty_order_items"),
                expr("cast(round(sum(price), 2) AS decimal(17, 2)) AS sum_price_order"),
                expr("cast(round(avg(price), 2) as decimal(17, 2)) AS avg_price_order"),
                expr("cast(round(min(price), 2) as decimal(17, 2)) AS min_price_order_item"),
                expr("cast(round(max(price), 2) as decimal(17, 2)) AS max_price_order_item"),
                expr("cast(round(avg(freight_value), 2) as decimal(17, 2)) AS avg_freight_value_order"),
                expr("to_timestamp(max(shipping_limit_date), 'yyyy-MM-dd HH:mm:ss') AS max_order_shipping_limit_date") 
            )

            return df_order_items_stats

        except Exception as e:
            logger.error("Erro ao preparar DAG de transformações para a base "
                         f"df_order_items. Exception: {e}")
            raise e

    # Método de transformação: customers
    def transform_customers(self, df: DataFrame) -> DataFrame:
        """
        Método de preparação do DataFrame df_customers.
        As etapas de transformação são dadas por:

        1. Seleção de atributos específicos a serem utilizados

        O método recebe e retorna objetos do tipo DataFrame Spark.
        """

        logger.info("Preparando DAG de transformações para df_customers")
        try:
            # Retornando dados utilizados da base de clientes
            df_customers_prep = df.selectExpr(
                "customer_id",
                "customer_city",
                "customer_state"
            )

            return df_customers_prep

        except Exception as e:
            logger.error("Erro ao preparar DAG de transformações para a base "
                         f"df_customers. Exception: {e}")
            raise e

    # Método de transformação: payments
    def transform_payments(self, df: DataFrame) -> DataFrame:
        """
        Método de preparação do DataFrame df_payments.
        As etapas de transformação são dadas por:

        1. Extração do "pagamento mais comum" para cada id de pedido
        2. Extração de agregados de pagamentos para cada id de pedido
        3. Join entre os dois dfs extraídos para retorno de df único.

        O método recebe e retorna objetos do tipo DataFrame Spark.
        """

        logger.info("Preparando DAG de transformações para df_payments")
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
            logger.error("Erro ao preparar DAG de transformações para a base "
                         f"df_payments. Exception: {e}")
            raise e

    # Método de transformação: reviews
    def transform_reviews(self, df: DataFrame) -> DataFrame:
        """
        Método de preparação do DataFrame df_reviews.
        As etapas de transformação são dadas por:

        1. Filtragem de reviews com order_id não nulo e score válido
        2. Seleção e transformação de campos utilizados
        3. Agrupamento de melhor score para cada order_id
        4. Eliminação de dados duplicados por order_id

        O método recebe e retorna objetos do tipo DataFrame Spark.
        """

        logger.info("Preparando DAG de transformações para df_reviews")
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
            logger.error("Erro ao preparar DAG de transformações para a base "
                         f"df_reviews. Exception: {e}")
            raise e

    # Método de transformação: tabela final
    def transform_sot(self, **kwargs) -> DataFrame:
        """
        Transformação completa da SoT através da unificação dos
        DataFrames preparados individualmente a partir de
        métodos específicos de transformação. A sequência
        de etapas para geração dos dados finais é dada por:

        1. Extração de DataFrames individuais dos argumentos
        2. Aplicação de join entre df_orders_prep e todos os
        demais DataFrames através das chaves relacionadas
        3. Geração de DataFrame final com atributos relacionados
        à características de pedidos feitos online (order_id)
        """

        # Desempacotando DataFrames dos argumentos da função
        df_orders_prep = kwargs["df_orders_prep"]
        df_order_items_prep = kwargs["df_order_items_prep"]
        df_customers_prep = kwargs["df_customers_prep"]
        df_payments_prep = kwargs["df_payments_prep"]
        df_reviews_prep = kwargs["df_reviews_prep"]

        # Gerando base final com atributos enriquecidos
        logger.info("Preparando DAG para geração de tabela final enriquecida")
        try:
            # Aplicando join entre todas as tabelas
            df_sot_join = df_orders_prep.join(
                other=df_order_items_prep,
                on=[df_orders_prep.order_id == df_order_items_prep.order_id]
            ).drop(df_order_items_prep.order_id).join(
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

            # Realizando seleção final nos dados
            df_sot_prep = df_sot_join.selectExpr(
                "order_id",
                "customer_id",
                "order_status",
                "order_purchase_timestamp",
                "order_approved_at",
                "order_delivered_carrier_date",
                "order_delivered_customer_date",
                "order_estimated_delivery_date",
                "year_order_purchase_timestamp",
                "quarter_order_purchase_timestamp",
                "month_order_purchase_timestamp",
                "dayofmonth_order_purchase_timestamp",
                "dayofweek_order_purchase_timestamp",
                "dayofyear_order_purchase_timestamp",
                "weekofyear_order_purchase_timestamp",
                "qty_order_items",
                "sum_price_order",
                "avg_price_order",
                "min_price_order_item",
                "max_price_order_item",
                "avg_freight_value_order",
                "max_order_shipping_limit_date",
                "customer_unique_id",
                "customer_zip_code_prefix",
                "customer_city",
                "customer_state",
                "installments",
                "sum_payments",
                "avg_payment_value",
                "distinct_payment_types",
                "most_common_payment_type",
                "review_best_score",
                "review_comment_message"
            )

        except Exception as e:
            logger.error("Erro ao preparar DAG para tabela final. "
                         f"Exception: {e}")
            raise e

        # Retornando base final
        return df_sot_prep

    # Encapsulando método único para execução do job
    def run(self) -> None:
        """
        Método responsável por consolidar todas as etapas de execução
        do job do Glue, permitindo assim uma maior facilidade e
        organização ao usuário final. Este método pode ser devidamente
        adaptado de acordo com as necessidades de cada usuário e de
        cada job a ser codificado, possibilitando uma centralização
        de todos os processos operacionais a serem realizados.
        Na prática, este método realiza as seguintes operações:

        1. Inicializa o job e obtém todos os insumos necessários
        2. Realiza a leitura dos objetos DataFrame/DynamicFrame
        3. Aplica as transformações necessárias
        4. Gerencia partições (elimina existente e adiciona uma nova)
        5. Escreve o resultado no s3 e cataloga no Data Catalog
        """

        # Preparando insumos do job
        job = self.init_job()

        # Lendo DynamicFrames e transformando em DataFrames Spark
        dfs_dict = self.generate_dataframes_dict()

        # Separando DataFrames em variáveis
        df_orders = dfs_dict["orders"]
        df_order_items = dfs_dict["order_items"]
        df_customers = dfs_dict["customers"]
        df_payments = dfs_dict["payments"]
        df_reviews = dfs_dict["reviews"]

        # Transformando dados
        df_orders_prep = self.transform_orders(df=df_orders)
        df_order_items_prep = self.transform_order_items(df=df_order_items)
        df_payments_prep = self.transform_payments(df=df_payments)
        df_reviews_prep = self.transform_reviews(df=df_reviews)

        # Gerando base final com atributos enriquecidos
        df_sot_prep = self.transform_sot(
            df_orders_prep=df_orders_prep,
            df_order_items_prep=df_order_items_prep,
            df_customers_prep=df_customers,
            df_payments_prep=df_payments_prep,
            df_reviews_prep=df_reviews_prep
        )

        # Criando variável de partição
        partition_value = int(datetime.now().strftime(
            self.args["PARTITION_FORMAT"]
        ))

        # Removendo partição física do S3
        self.drop_partition(
            partition_name=self.args["PARTITION_NAME"],
            partition_value=partition_value
        )

        # Adicionando coluna de partição ao DataFrame
        df_sot_prep_partitioned = self.add_partition(
            df=df_sot_prep,
            partition_name=self.args["PARTITION_NAME"],
            partition_value=partition_value
        )

        # Reparticionando DataFrame para otimizar armazenamento
        df_sot_prep_repartitioned = self.repartition_dataframe(
            df=df_sot_prep_partitioned,
            num_partitions=int(self.args["NUM_PARTITIONS"])
        )

        # Escrevendo e catalogando dados
        self.write_data_to_catalog(df=df_sot_prep_repartitioned)

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
        data_dict=DATA_DICT
    )

    # Executando todas as lógicas mapeadas do job
    glue_manager.run()
