"""
JOB: terraglue-job-sot-ecommerce-br.py

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
    "CREATE_SPARK_TEMP_VIEW"
]

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
    Classe responsável por gerenciar e fornecer todos os insumos
    necessários para a utilização de um job do Glue na dinâmica
    de processamento de dados. Com ela, o usuário final possui
    uma maior facilidade relacionada aos processos de obtenção
    de argumentos e geração dos contextos (GlueContext, SparkContext)
    e sessões (GlueContext.spark_session) necessárias para
    execução do job.

    Atributos requeridos:
    --------------------
    :attr: argv_list
        Lista contendo a referência nominal de todos os argumentos
        a serem utilizados durante o job a partir da função
        getResolvedOptions()
        [type: list, required=True]

    Atributos obtidos automaticamente:
    ----------------------------------
    :attr: args
        Dicionário contendo os argumentos do job extraídos pela
        função getResolvedOptions().
        [type: dict, required=False]

    :attr: sc
        Contexto do Spark criado durante os procedimentos internos da
        classe para posterior utilização nas etapas de construção
        de um job do Glue.
        [type: pyspark.context.SparkContext]

    :attr: glueContext
        Contexto do Glue criado a partir do contexto do Spark
        inicializado previamente. Este elemento é fundamental para
        operações internas de construção de um job do Glue.
        [type: awsglue.context.GlueContext]

    :attr spark
        Sessão Spark criada a partir do contexto do Glue para
        eventuais utilizações específicas dentro dos propósitos
        estabelecidos e as regras definidas no job.
        [type: SparkSession]
    """

    def __init__(self, argv_list: list) -> None:
        self.argv_list = argv_list
        self.args = getResolvedOptions(sys.argv, self.argv_list)

    # Obtendo argumentos do job
    def print_args(self) -> None:
        """
        Método responsável por mostrar ao usuário, como uma mensagem
        de log, todos os argumentos utilizados no referido job e
        seus respectivos valores.
        """

        try:
            args_formatted = "".join([f'--{k}: "{v}"\n'
                                      for k, v in self.args.items()])
            logger.info(f"Argumentos do job:\n\n{args_formatted}")
            sleep(0.01)
        except Exception as e:
            logger.error("Erro ao retornar argumentos do job dentro da "
                         f"lista informada. Exception: {e}")
            raise e

    # Obtendo elementos de contexto e sessão da aplicação
    def get_context_and_session(self) -> None:
        """
        Método responsável por criar e associar atributos da classe
        para os elementos SparkContext, GlueContext e SparkSession.
        """

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
        """
        Método criado para consolidar todas as etapas de inicialização
        de um job do Glue a partir da visualização dos argumentos e
        obtenção dos elementos de contexto e sessão. Com a execução
        deste método, o usuário poderá ter uma porta única de entrada
        para todos os processos relativamente burocráticos de configuração
        de um job do Glue.

        :return: job
            Elemento de job utilizado pelo Glue para configurações gerais
            [type: awsglue.job.Job]
        """

        # Obtendo argumentos e objetos de sessão
        self.print_args()
        self.get_context_and_session()

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
    Classe responsável por gerenciar e fornecer métodos típicos
    de transformação de um job do Glue a serem detalhadamente
    adaptados por seus usuários para que as operações nos dados
    possam ser aplicadas de acordo com as necessidades exigidas.

    Em essência, essa classe herda os atributos e métodos da
    classe GlueJobManager para que todas as operações de
    inicialização e configuração de um job do Glue possam ser
    aplicadas em conjunto às operações de transformação, mantendo
    uma porta única de entrada ao usuário final em meio à todos
    os processos exigidos para a construção de um job.

    Em linhas gerais, a classe GlueTransformationManager traz
    consigo dois tipos de métodos:
        1. Métodos gerais que podem ser aplicados em diferentes
    cenários
        2. Métodos específicos utilizados de acordo com as
    necessidades de transformações de dados de cada job

    Dessa forma, o usuário final possui em mãos algumas
    funcionalidades genéricas que podem ser reaproveitadas para
    grande parte dos jobs do Glue. Entretanto, métodos específicos
    de transformação devem ser modificados e adaptados conforme
    as regras definidas a serem aplicadas pelo usuário de acordo
    com os objetivos estabelecidos. Considerando a versão natural
    desta classe, os métodos específicos de transformação podem
    ser identificados através do decorator @staticmethod, indicando
    assim que o método em questão é um método específico de
    transformação que não utiliza ou acessa nenhum atributo da classe.

    Atributos requeridos:
    --------------------
    :attr: argv_list
        Lista contendo a referência nominal de todos os argumentos
        a serem utilizados durante o job a partir da função
        getResolvedOptions()
        [type: list, required=True]

    :attr: data_dict
        Dicionário contento todas as especifidades dos dados de
        origem a serem utilizados como fontes de dados do job. Tal
        dinâmica visa proporcionar uma maior facilidade ao usuário
        para gerenciar todos os processos de leitura e obtenção de
        DynamicFrames do Glue ou DataFrames do Spark através de
        métodos únicos. Um exemplo de configuração deste atributo
        pode ser visualizado abaixo:

        {
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

        Caso o usuário deseje uma configuração específica, basta
        consultar os argumentos do método
        glueContext.create_dynamic_frame.from_catalog para que o
        dicionário seja passado corretamente. Parâmetros como
        push_down_predicate, additional_options e catalog_id
        também podem ser configurados como chaves deste dicionário e,
        caso não informados, seus respectivos valores default,
        presentes na documentação, serão utilizados.
    """

    def __init__(self, argv_list: list, data_dict: dict) -> None:
        self.argv_list = argv_list
        self.data_dict = data_dict

        # Herdando atributos de classe de gerenciamento de job
        GlueJobManager.__init__(self, argv_list=self.argv_list)

    # Gerando dicionário de DynamicFrames do projeto
    def generate_dynamic_frames_dict(self) -> dict:
        """
        Método responsável por utilizar o atributo data_dict da classe
        para leitura e obtenção de todos os DynamicFrames configurados
        no referido dicionário de acordo com as especificações
        fornecidas. A grande vantagem deste método é a disponibilização
        dos DynamicFrames como elementos de um dicionário Python que,
        posteriormente, podem ser acessados em outras etapas do código
        para o mapeamento das operações. Esta dinâmica evita que o
        usuário precise codificar um bloco específico de leitura para
        cada origem de dados do job, possibilitando que o usuário apenas
        acesse cada uma das suas origens através de uma indexação.

        :return: dynamic_dict
            Dicionário Python contendo um mapeamento de cada uma das
            origens configuradas no atributo self.data_dict e seus
            respectivos objetos do tipo DynamicFrame. Para proporcionar
            uma visão clara sobre o retorno deste método, considere,
            como exemplo, a seguinte configuração para o atributo
            self.data_dict:

            {
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

            O retorno do método generate_dynamic_frames_dict() será
            no seguinte formato:

            {
                "orders": <DynamicFrame>
                "customers": <DynamicFrame>
            }

            onde as tags <DynamicFrame> representam o objeto do tipo
            DynamicFrame lido para cada origem, utilizando as
            configurações apresentadas no dicionário do atributo
            self.data_dict e disponibilizado ao usuário dentro da
            respectiva chave que representa a origem.
        """

        logger.info("Iterando sobre dicionário de dados fornecido para " +
                    "leitura de DynamicFrames do Glue")
        try:
            dynamic_frames = []
            for t in self.data_dict.keys():
                # Coletando argumentos obrigatórios: database, table_name, ctx
                database = self.data_dict[t]["database"]
                table_name = self.data_dict[t]["table_name"]
                transformation_ctx = self.data_dict[t]["transformation_ctx"]

                # Coletando argumento não obrigatório: push_down_predicate
                push_down_predicate = self.data_dict[t]["push_down_predicate"]\
                    if "push_down_predicate" in self.data_dict[t].keys()\
                    else ""

                # Coletando argumento não obrigatório: additional_options
                additional_options = self.data_dict[t]["additional_options"] \
                    if "additional_options" in self.data_dict[t].keys()\
                    else {}

                # Coletando argumento não obrigatório: catalog_id
                catalog_id = self.data_dict[t]["catalog_id"] \
                    if "catalog_id" in self.data_dict[t].keys()\
                    else None

                # Lendo DynamicFrame
                dyf = self.glueContext.create_dynamic_frame.from_catalog(
                        database=database,
                        table_name=table_name,
                        transformation_ctx=transformation_ctx,
                        push_down_predicate=push_down_predicate,
                        additional_options=additional_options,
                        catalog_id=catalog_id
                )

                # Adicionando à lista de DynamicFrames
                dynamic_frames.append(dyf)
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
        """
        Método responsável por consolidar os processos necessários
        para disponibilização, ao usuário, de objetos do tipo DataFrame
        Spark capazes de serem utilizados nas mais variadas etapas
        de transformação do job Glue. Na prática, este método chama o
        método generate_dynamic_frames_dict() para coleta dos objetos do
        tipo DynamicFrame (ver documentação acima) e, na sequência, aplica
        o método toDF() para transformação de tais objetos em objetos
        do tipo DataFrame Spark.

        :return: dataframe_dict
            Dicionário Python contendo um mapeamento de cada uma das
            origens configuradas no atributo self.data_dict e seus
            respectivos objetos do tipo DataFrame. Para proporcionar
            uma visão clara sobre o retorno deste método, considere,
            como exemplo, a seguinte configuração para o atributo
            self.data_dict:

            {
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

            O retorno do método generate_dataframes_dict() será
            no seguinte formato:

            {
                "orders": <DataFrame>
                "customers": <DataFrame>
            }

            onde as tags <DataFrame> representam o objeto do tipo
            DataFrame lido para cada origem, utilizando as
            configurações apresentadas no dicionário do atributo
            self.data_dict e disponibilizado ao usuário dentro da
            respectiva chave que representa a origem.
        """

        # Gerando dicionário de DynamicFrames
        dyf_dict = self.generate_dynamic_frames_dict()

        # Transformando DynamicFrames em DataFrames
        logger.info(f"Transformando os {len(dyf_dict.keys())} "
                    "DynamicFrames em DataFrames Spark")
        try:
            df_dict = {k: dyf.toDF() for k, dyf in dyf_dict.items()}
            logger.info("DataFrames Spark gerados com sucesso")
            sleep(0.01)
        except Exception as e:
            logger.error("Erro ao transformar DynamicFrames em "
                         f"DataFrames Spark. Exception: {e}")
            raise e

        # Validando parâmetro para criação de temp views para os DataFrames
        if bool(self.args["CREATE_SPARK_TEMP_VIEW"]):
            logger.info("Criando tabelas temporárias para os "
                        f"{len(dyf_dict.keys())} DataFrames Spark")
        
            for k, v in self.data_dict.items():
                try:
                    # Extraindo variáveis
                    df = df_dict[k]
                    table_name = v["table_name"]

                    # Criando tabela temporária
                    df.createOrReplaceTempView(table_name)
                except Exception as e:
                    logger.error("Erro ao criar tabela temporária "
                                 f"{table_name}. Exception: {e}")
                    raise e

        # Retornando dicionário de DataFrames Spark convertidos
        return df_dict

    # Método de transformação: payments
    def transform_payments(self, df: DataFrame) -> DataFrame:
        """
        Método de transformação específico para uma das origens
        do job do Glue.

        Parâmetros
        ----------
        :param: df
            DataFrame Spark alvo das transformações aplicadas.
            [type: pyspark.sql.DataFrame]

        Retorno
        -------
        :return: df_prep
            Elemento do tipo DataFrame Spark após as transformações
            definidas pelos métodos aplicadas dentro da DAG.
            [type: DataFrame]
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
    def transform_reviews(self, df: DataFrame) -> DataFrame:
        """
        Método de transformação específico para uma das origens
        do job do Glue.

        Parâmetros
        ----------
        :param: df
            DataFrame Spark alvo das transformações aplicadas.
            [type: pyspark.sql.DataFrame]

        Retorno
        -------
        :return: df_prep
            Elemento do tipo DataFrame Spark após as transformações
            definidas pelos métodos aplicadas dentro da DAG.
            [type: DataFrame]
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
    def transform_sot(self, **kwargs) -> DataFrame:
        """
        Método de transformação específico para uma das origens
        do job do Glue.

        Parâmetros
        ----------
        :param: df
            DataFrame Spark alvo das transformações aplicadas.
            [type: pyspark.sql.DataFrame]

        Retorno
        -------
        :return: df_prep
            Elemento do tipo DataFrame Spark após as transformações
            definidas pelos métodos aplicadas dentro da DAG.
            [type: DataFrame]
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

    # Método de transformação: drop de partição física no s3
    def drop_partition(self, partition_name: str,
                       partition_value: str,
                       retention_period: int = 0) -> None:
        """
        Método responsável por eliminar partições do s3 através
        do delete físico dos arquivos armazenados em um
        determinado prefixo. Em essência, este método pode ser
        utilizado em conjunto com o método de adição de partições,
        garantindo a não geração de dados duplicados em uma
        mesma partição em casos de dupla execução do job.
        Para o processo de eliminação física dos arquivos, o
        método purge_s3_path do glueContext é utilizado.

        Parâmetros
        ----------
        :param partition_name:
            Nome da partição (primeira parte do prefixo no s3)
            a ser eliminada.
            [type: str]
        
        :param partition_value:
            Valor da partição (segunda parte do prefixo s3)
            a ser eliminada.
            [type: str]
        """
        
        # Montando URI da partição a ser eliminada
        partition_uri = f"s3://{self.args['OUTPUT_BUCKET']}/"\
            f"{self.args['OUTPUT_DB']}/{self.args['OUTPUT_TABLE']}/"\
            f"{partition_name}={partition_value}/"

        logger.info(f"Eliminando partição {partition_name}={partition_value} "
                    f"através da URI {partition_uri}")
        try:
            self.glueContext.purge_s3_path(
                s3_path=partition_uri,
                options={"retentionPeriod": retention_period}
            )
        except Exception as e:
            logger.error("Erro ao eliminar partição "
                         f"{partition_name}={partition_value}. Exception: {e}")
            raise e
    
    # Método de transformação: adição de partição
    @staticmethod
    def add_partition(df: DataFrame,
                      partition_name: str,
                      partition_value: str) -> DataFrame:
        """
        Método responsável por adicionar uma coluna ao DataFrame
        resultante para funcionar como partição da tabela gerada.
        Na prática, este método utiliza o método .withColumn() do
        pyspark para adição de uma coluna considerando um nome
        de atributo (partition_name) e seu respectivo valor
        (partition_value).

        Parâmetros
        ----------
        :param: df
            DataFrame Spark alvo das transformações aplicadas.
            [type: pyspark.sql.DataFrame]

        :param: partition_name
            Nome da partição considerada como um novo atributo da
            base de dados alvo.
            [type: string]

        :param: partition_value
            Valor para a respectiva partição.
            [type: any]
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
        Método responsável por consolidar todas as etapas necessárias
        para escrita de dados no s3 e a subsequente catalogação no Data
        Catalog. Para toda a configuração necessária para execução das
        etapas de escrita e catalogação, parâmetros do job são utilizados
        diretamente do atributo self.args da classe instanciada. Dessa
        forma, é extremamente importante validar se todos os atributos
        aplicados neste método foram devidamente fornecidos ou configurados
        pelo usuário, seja pelo próprio script ou por um pipeline de IaC
        (ex: terraform). Em essência, este método realiza as seguintes
        operações:
            1. Verificação se o conjunto de dados fornecido como argumento
            é do tipo DynamicFrame (caso contrário, converte)
            2. Faz um sink com o catálogo de dado
            3. Escreve dados no s3 e atualiza catálogo de dados

        Parâmetros
        ----------
        :param: df
            Objeto do tipo DataFrame ou DynamicFrame a ser utilizado como
            alvo de escrita e catalogação. Os métodos utilizados para
            escrita e catalogação consideram um objeto do tipo DynamicFrame
            como alvo e, assim sendo, existe uma validação inicial neste
            método codificada para validar se o objeto passado é do tipo
            DynamicFrame. Caso contrário, uma conversão é realizada para que
            os métodos subsequentes possam ser executados.
            [type: DataFrame or DynamicFrame]
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
            # Criando variável de saída com base em argumentos do job
            output_path = f"s3://{self.args['OUTPUT_BUCKET']}/"\
                f"{self.args['OUTPUT_DB']}/{self.args['OUTPUT_TABLE']}"

            # Criando relação de escrita de dados
            data_sink = self.glueContext.getSink(
                path=output_path,
                connection_type=self.args["CONNECTION_TYPE"],
                updateBehavior=self.args["UPDATE_BEHAVIOR"],
                partitionKeys=[self.args["PARTITION_NAME"]],
                compression=self.args["COMPRESSION"],
                enableUpdateCatalog=bool(self.args["ENABLE_UPDATE_CATALOG"]),
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
                catalogDatabase=self.args["OUTPUT_DB"],
                catalogTableName=self.args["OUTPUT_TABLE"]
            )
            data_sink.setFormat(self.args["DATA_FORMAT"], useGlueParquetWriter=True)
            data_sink.writeFrame(dyf)

            logger.info(f"Tabela {self.args['OUTPUT_DB']}."
                        f"{self.args['OUTPUT_TABLE']} "
                        "atualizada com sucesso no catálogo. Seus dados estão "
                        f"armazenados em {output_path}")
        except Exception as e:
            logger.error("Erro ao adicionar entrada para tabela no catálogo "
                         f"de dados. Exception: {e}")
            raise e

    # Encapsulando método único para execução do job
    def run(self) -> None:
        """
        Método responsável por consolidar todas as etapas de execução
        do job do Glue, permitindo assim uma maior facilidade e
        organização ao usuário final. Este método pode ser devidamente
        adaptado de acordo com as necessidades de cada usuário e de
        cada job a ser codificado, possibilitando uma centralização
        de todos os processos operacionais a serem realizados. Com isso,
        um melhor gerenciamento do job pode ser obtido, visto que, no
        programa principal, o usuário terá apenas que executar o método
        run(). Na prática, este método realiza as seguintes operações:

            1. Inicializa o job e obtém todos os insumos necessários
            2. Realiza a leitura dos objetos DataFrame
            3. Aplica as transformações necessárias
            4. Adiciona uma partição de data aos dados
            5. Escreve o resultado no s3 e cataloga no Data Catalog
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
        partition_value = datetime.now().strftime(
            self.args["PARTITION_FORMAT"]
        )
        df_sot_prep_partitioned = self.add_partition(
            df=df_sot_prep,
            partition_name=self.args["PARTITION_NAME"],
            partition_value=partition_value
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
        data_dict=DATA_DICT
    )

    # Executando todas as lógicas mapeadas do job
    glue_manager.run()
