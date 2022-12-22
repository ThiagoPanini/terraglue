"""
MODULE: terraglue.py

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
from time import sleep
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import DataFrame
from pyspark.sql.functions import lit


# Função para configuração de log
def log_config(logger_name: str = __file__,
               logger_level: int = logging.INFO,
               logger_date_format: str = "%Y-%m-%d %H:%M:%S") -> None:
    """
    Função criada para facilitar a criação de configuração
    de uma instância de Logger do Python utilizada no
    decorrer da aplicação Spark para registros de logs
    das atividades e das funcionalidades desenvolvidas.

    Parâmetros
    ----------
    :param logger_name:
        Nome da instância de logger.
        [type: str, default="glue_logger"]

    :param logger_level:
        Nível dos registros de log configurado.
        [type: int, default=logging.INFO]

    :param logger_date_format:
        Formato de data configurado para representação
        nas mensagens de logs.
        [type: str, default="%Y-%m-%d %H:%M:%S"]
    """

    # Instanciando objeto de logging
    logger = logging.getLogger(logger_name)
    logger.setLevel(logger_level)

    # Configurando formato das mensagens no objeto
    log_format = "%(levelname)s;%(asctime)s;%(filename)s;"
    log_format += "%(lineno)d;%(message)s"
    formatter = logging.Formatter(log_format,
                                  datefmt=logger_date_format)

    # Configurando stream handler do objeto de log
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


# Configurando objeto de log
logger = log_config(logger_name=__file__)


# Classe para gerenciamento de insumos de um job Glue
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

    def __init__(self, argv_list: list,
                 data_dict: dict) -> None:
        self.argv_list = argv_list
        self.data_dict = data_dict
        self.args = getResolvedOptions(sys.argv, self.argv_list)

    # Preparando mensagem inicial para início do job
    def job_initial_log_message(self) -> None:
        """
        Método responsável por compor uma mensagem inicial de log a ser
        consolidada no CloudWatch sempre que um objeto desta classe
        for instanciado. A mensagem de log visa declarar todas as
        origens utilizadas no job Glue, além de fornecer detalhes
        sobre os push down predicates (se utilizados) em cada
        processo de leitura de dados.
        """

        # Definindo strings para casos com ou sem push down predicate
        without_pushdown = "sem push down predicate definido"
        with_pushdown = "com push down predicate definido por <push_down>"

        # Definindo strings iniciais para composição da mensagem
        welcome_msg = f"Iniciando execução de job {self.args['JOB_NAME']}. "\
                      "Origens presentes no processo de ETL:\n\n"
        template_msg = f"Tabela <tbl_ref> {without_pushdown}{with_pushdown}\n"
        initial_msg = ""

        # Iterando sobre dicionário de dados para extração de parâmetros
        for _, params in self.data_dict.items():
            # Iniciando preparação da mensagem inicial
            initial_msg += template_msg

            # Obtendo tabela e substituindo em template
            tbl_ref = f"{params['database']}.{params['table_name']}"
            initial_msg = initial_msg.replace("<tbl_ref>", tbl_ref)

            # Validando existência de push_down_predicate
            if "push_down_predicate" in params:
                push_down = params["push_down_predicate"]
                initial_msg = initial_msg.replace(without_pushdown, "")
                initial_msg = initial_msg.replace("<push_down>", push_down)
            else:
                initial_msg = initial_msg.replace(with_pushdown, "")

        # Adicionando mensagem de boas vindas
        initial_msg = welcome_msg + initial_msg
        logger.info(initial_msg)

    # Obtendo e logando argumentos do job
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

        # Obtendo argumentos e consolidando mensagens de log
        self.job_initial_log_message()
        self.print_args()

        # Obtendo elementos de sessão e conteto Spark e Glue
        self.get_context_and_session()

        # Inicializando objeto de Job do Glue
        try:
            job = Job(self.glueContext)
            job.init(self.args['JOB_NAME'], self.args)
            return job
        except Exception as e:
            logger.error(f"Erro ao inicializar job do Glue. Exception: {e}")
            raise e


# Classe para o gerenciamento de transformações Spark em um job
class GlueETLManager(GlueJobManager):
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
        GlueJobManager.__init__(self, argv_list=self.argv_list,
                                data_dict=self.data_dict)

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
                    "transformation_ctx": "dyf_orders"
                },
                "customers": {
                    "database": "ra8",
                    "table_name": "customers",
                    "transformation_ctx": "dyf_customers",
                    "push_down_predicate": "anomesdia=20221201",
                    "create_temp_view": True,
                    "additional_options": {
                        "compressionType": "lzo"
                    }
                }
            }

            Todos os parâmetros presentes no método
            glueContext.create_dynamic_frame.from_catalog() são
            aceitos na construção do dicionário self.data_dict.
            Além disso, alguns parâmetros adicionais foram inclusos
            visando proporcionar uma maior facilidade aos usuários,
            como por exemplo:
                * "create_temp_view": bool -> configura a criação
                    de uma tabela temporária (view) para a tabela
                    em questão

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
                    "transformation_ctx": "dyf_orders"
                },
                "customers": {
                    "database": "ra8",
                    "table_name": "customers",
                    "transformation_ctx": "dyf_customers",
                    "push_down_predicate": "anomesdia=20221201",
                    "create_temp_view": True,
                    "additional_options": {
                        "compressionType": "lzo"
                    }
                }
            }

            Todos os parâmetros presentes no método
            glueContext.create_dynamic_frame.from_catalog() são
            aceitos na construção do dicionário self.data_dict.
            Além disso, alguns parâmetros adicionais foram inclusos
            visando proporcionar uma maior facilidade aos usuários,
            como por exemplo:
                * "create_temp_view": bool -> configura a criação
                    de uma tabela temporária (view) para a tabela
                    em questão

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

        # Iterando sobre dicionário de dados para validar criação de temp views
        for table_key, params in self.data_dict.items():
            try:
                # Extraindo variáveis
                df = df_dict[table_key]
                table_name = params["table_name"]

                # Criando tabela temporária (se aplicável)
                if "create_temp_view" in params\
                        and bool(params["create_temp_view"]):
                    df.createOrReplaceTempView(table_name)

                    logger.info(f"Tabela temporária (view) {table_name} "
                                "criada com sucesso.")

            except Exception as e:
                logger.error("Erro ao criar tabela temporária "
                             f"{table_name}. Exception: {e}")
                raise e

        # Retornando dicionário de DataFrames Spark convertidos
        return df_dict

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
            data_sink.setFormat(self.args["DATA_FORMAT"],
                                useGlueParquetWriter=True)
            data_sink.writeFrame(dyf)

            logger.info(f"Tabela {self.args['OUTPUT_DB']}."
                        f"{self.args['OUTPUT_TABLE']} "
                        "atualizada com sucesso no catálogo. Seus dados estão "
                        f"armazenados em {output_path}")
        except Exception as e:
            logger.error("Erro ao adicionar entrada para tabela no catálogo "
                         f"de dados. Exception: {e}")
            raise e
