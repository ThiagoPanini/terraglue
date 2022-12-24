"""
SCRIPT: spark_helper.py

CONTEXTO:
---------
Script criado para facilitar algumas operações úteis
para consolidar testes de aplicações Spark em jobs Glue.
Em essência, as funções e todo o código aqui presente
pode ser utilizado, principalmente, na geração de dados
fictícios presentes como Spark DataFrames para a criação
de elementos que podem ser utilizados nas mais variadas
operações de testes.


OBJETIVO:
---------
Consolidar regras e códigos úteis capazes de proporcionar,
ao usuário, funções prontas para a criação de DataFrames
Spark, schemas, dados fictícios ou qualquer outro insumo
que possa facilitar o desenvolvimento de testes unitários.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Bibliotecas utilizadas no módulo
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructField, StructType, StringType
from faker import Faker
from decimal import Decimal
from random import randrange


"""---------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.2 Definindo variáveis e objetos
---------------------------------------------------"""

# Inicializando faker para geração de dados fictícios
faker = Faker()


"""---------------------------------------------------
---------- 2. FUNÇÕES PARA GERAÇÃO DE DADOS ----------
              2.1 Gerando dados ficítios
---------------------------------------------------"""


# Criando e retornando objeto de sessão Spark
def create_spark_session() -> SparkSession:
    return SparkSession.builder.getOrCreate()


# Gerando schema Spark através de dicionário de metadados
def generate_schema_from_dict(schema_dict: dict,
                              nullable: bool = True) -> StructType():
    """
    Função criada para gerar um schema para DataFrames Spark
    do tipo StructType com base em dicionário contendo nomes
    de campos e tipos primitivos fornecido pelo usuário.
    Na prática, o usuário pode ter em mãos informações já
    consolidadas sobre a base de dados a ser gerada de forma
    artificial, permitindo assim uma maior facilidade e
    garantia de que os dados gerados seguirão um schema pré
    definido.

    Parâmetros
    ----------
    :param schema_dict:
        Dicionário Python contendo referências para os
        nomes das colunas (chaves) e seus respectivos
        tipos primitivos (valores) a serem utilizados no
        processo de criação de um schema StructType().

        Para isso, basta que o usuário construa um
        dicionário Python no seguinte formato para inserção no
        parâmetro schema_dict da função:

        # Exemplo de schema_dict
        schema_dict = {
            "foo": StringType(),
            "bar": IntegerType(),
            "baz": DecimalType(17, 2),
            "qux": BooleanType()
        }

    :param nullable:
        Parâmetro nullable do processo de criação de schema
        que define se o determinado campo pode obter valores
        nulos.
        [type: bool, default=True]

    Retorno
    -------
    :return schema:
        Schema do tipo StructType() criado a partir da
        iteração com o dicionário fornecido pelo usuário
        e a posterior extração e consolidação dos nomes
        dos atributos e seus respectivos tipos primitivos.
    """

    return StructType([
        StructField(col, dtype, nullable)
        for col, dtype in schema_dict.items()
    ])


# Gerando schema Spark através de lista de atributos
def generate_schema_from_list(schema_list: list,
                              schema_dtype: type = StringType(),
                              nullable: bool = True) -> StructType():
    """
    Função criada para gerar um schema para DataFrames Spark
    do tipo StructType com base em uma lista Python contendo
    apenas os nomes dos campos a serem criados em um posterior
    processo de geração de DataFrame. Este método pode ser
    utilizado caso o usuário não tenha restrições sobre
    mapear um tipo primitivo específico para cada campo, mas
    sim um tipo primitivo único para todos os campos (processo
    guiado pelo parâmetro schema_dtype).

    Parâmetros
    ----------
    :param schema_list:
        List Python contendo referências para os nomes das
        colunas a serem utilizadas no processo de criação
        de um schema StructType().

        Exemplo de input para este parâmetro:

        schema_list = ["foo", "bar", "barz", "qux"]

    :param schema_dytpe:
        Como este método não possui qualquer referência ou
        mapeamento de tipos primitivos para cada uma das
        colunas fornecidas na lista, é preciso informar um
        tipo primitivo padrão e único a ser utilizado no
        processo de criação de schema. O parâmetro
        schema_dtype traz essa funcionalidade e permite que
        o usuário crie, por exemplo, um schema com todos
        os atributos do tipo StringType(), ou IntegerType(),
        ou então de qualquer outro tipo primitivo de sua
        escolha.
        [type: type, default=StringType()]

    :param nullable:
        Parâmetro nullable do processo de criação de schema
        que define se o determinado campo pode obter valores
        nulos.
        [type: bool, default=True]

    Retorno
    -------
    :return schema:
        Schema do tipo StructType() criado a partir da
        iteração com o dicionário fornecido pelo usuário
        e a posterior extração e consolidação dos nomes
        dos atributos e seus respectivos tipos primitivos.
    """

    return StructType([
        StructField(col, schema_dtype, nullable)
        for col in schema_list
    ])


# Gerando dados fictícios a partir de schema Spark
def generate_fake_data_from_schema(schema: StructType(),
                                   num_rows: int = 5) -> tuple:
    """
    Função criada para consolidar todo o processo de geração
    de dados fictícios para posterior inserção em um
    DataFrame Spark em conjunto com um schema StructType()
    definido previamente. Em essência, as regras dessa
    função envolvem a utilização da biblioteca Faker()
    com base em validações pontuais sobre cada um
    dos tipos primitivos de um schema fornecido pelo
    usuário. Para cada tipo encontrado, um tipo de dado
    fictício é gerado e anexado à uma lista até que um
    único registro seja completamente definido. O processo
    é então repetido de acordo com a quantidade de registros
    a serem criados (parâmetro num_rows), gerando assim
    uma lista de registros que, posteriormente, é transformada
    em uma lista de tuplas para adequação ao processo de
    criação de DataFrames Spark.

    Parâmetros
    ----------
    :param schema:
        Schema StructType() utilizado no processo de iteração
        de tipos primitivos para geração de dados fictícios
        adequados para cada elemento.
        [type: StructType()]

    :param num_rows:
        Quantidade de registros a serem gerados no processo
        de iteração.
        [type: int, default=5]

    Retorno
    -------
    :return fake_data:
        Lista de tuplas contendo dados fictícios gerados com
        base em cada um dos tipos primitivos presentes no
        schema fornecido. O formado de lista já está
        automaticamente adequado para ser utilizado no processo
        de criação de DataFrames Spark.
        [type: list[tuple]]
    """

    fake_data = []
    for i in range(num_rows):
        # Iterando sobre colunas e construindo registro
        fake_row = []
        for field in schema:
            dtype = field.dataType.typeName()
            if dtype == "string":
                fake_row.append(faker.word())
            elif dtype == "integer":
                fake_row.append(randrange(1, 100000))
            elif dtype == "decimal":
                fake_row.append(Decimal(randrange(1, 100000)))
            elif dtype == "boolean":
                fake_row.append(faker.boolean())

        # Adicionando registro na lista de registros
        fake_data.append(fake_row)

    return [tuple(row) for row in fake_data]


# Gerando e retornando DataFrame Spark
def generate_spark_dataframe(spark: SparkSession,
                             schema_input: list or dict,
                             schema_dtype: type = StringType(),
                             nullable: bool = True,
                             num_rows: int = 5) -> DataFrame:
    """
    Função criada para consolidar todo o processo de geração
    de um DataFrame Spark com dados fictícios a partir de
    informações sobre metadados fornecidas pelo usuário,
    sejam estas dadas através de um dicionário contendo
    nomes de atributos e tipos primitivos, ou através de
    uma lista contendo apenas nomes de atributos e um
    tipo primitivo comum para todos. Esta função é
    responsável por chamar as demais funções deste módulo
    com base em validações e regras internas criadas para
    garantir que o usuário possua um canal único para o
    alcance de seu objetivo: a geração de DataFrames Spark
    para testes e validações.

    Parâmetros
    -----------
    :param spark:
        Objeto de sessão Spark utilizado para a execução
        do processo de criação de DataFrames.
        [type: SparkSession]

    :param schema_input:
        Schema definido pelo usuário para a criação do
        DataFrame desejado. Este parâmetro pode ser definido
        com base em um dicionário (ver descrição do argumento
        schema_dict da função generate_schema_from_dict() ou
        então com base em uma lista (ver descrição do argumento
        schema_list da função generate_schema_from_list())).
        Internamente, esta função valida o tipo primitivo deste
        parâmetro para, assim, chamar a função mais adequada
        para geração do schema StructType() utilizado nos
        passos posteriores.
        [type: list or dict]

    :param schema_dtype:
        Caso o usuário forneça uma lista de atributos para o
        parâmetro schema_input, é necessário garantir a
        definição de um tipo primitivo comum para criação
        do schema. Para maiores detalhes, analisar o argumento
        schema_dtype da função generate_schema_from_list().
        [type: type, default=StringType()]

    :param nullable:
        Parâmetro nullable do processo de criação de schema
        que define se o determinado campo pode obter valores
        nulos.
        [type: bool, default=True]

    :param num_rows:
        Quantidade de registros a serem gerados no processo
        de iteração.
        [type: int, default=5]

    Retorno
    -------
    :return df:
        DataFrame Spark contendo os dados fictícios mapeados
        através do parâmetro schema_input fornecido pelo
        usuário.
        [type: DataFrame]
    """

    if type(schema_input) is dict:
        # Gerando schema com base em dicionário
        schema = generate_schema_from_dict(
            schema_dict=schema_input,
            nullable=nullable
        )
    else:
        # Gerando schema com base em lista de colunas
        schema = generate_schema_from_list(
            schema_list=schema_input,
            schema_dtype=schema_dtype,
            nullable=nullable
        )

    # Gerando dados fictícios
    data = generate_fake_data_from_schema(schema, num_rows)

    # Retornando DataFrame Spark
    return spark.createDataFrame(data=data, schema=schema)
