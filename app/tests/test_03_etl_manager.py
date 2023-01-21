"""
SCRIPT: test_etl_manager.py

CONTEXTO:
---------
Script de testes criado para validar elementos e
funcionalidades presentes na classe GlueETLManager do
módulo terraglue como forma de garantir que todos os
insumos necessários para execução da aplicação Spark
se fazem presentes.

OBJETIVO:
---------
Consoldar uma suíte de testes capaz de testar e validar
todos os insumos presentes na classe GlueETLManager que
podem comprometer o funcionamento da aplicação.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Importando módulos para uso
import pytest
from datetime import datetime
from pyspark.sql.types import StringType, DateType, TimestampType
# from moto import mock_glue


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


@pytest.mark.etl_manager
@pytest.mark.date_attributes_extraction
def test_conversao_de_data_no_metodo_de_extracao_de_atributos_de_data(
    etl_manager, fake_dataframe, date_col="date", date_col_type="date",
    date_test_col_name="date_test", date_format='%Y-%m-%d'
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método date_attributes_extraction() da classe
       GlueETLManager for executado em uma coluna de data com
       date_col_type="date" e convert_string_to_date=True
    T: então o DataFrame resultante deve conter a mesma coluna de data
       porém com o tipo primitivo DateType
    """

    # Aplicando casting forçado de campo de data para string
    fake_dataframe_cast = fake_dataframe.selectExpr(
        "*",
        f"cast({date_col} AS STRING) AS {date_test_col_name}"
    )

    # Executando método de extração de atributos de data
    fake_df_prep = etl_manager.date_attributes_extraction(
        df=fake_dataframe_cast,
        date_col=date_test_col_name,
        date_col_type=date_col_type,
        date_format=date_format,
        convert_string_to_date=True
    )

    # Extraindo informações antes da conversão
    dtype_pre_casting = fake_dataframe_cast\
        .schema[date_test_col_name].dataType

    # Extraindo tipo do campo após a conversão
    dtype_pos_casting = fake_df_prep\
        .schema[date_test_col_name].dataType

    # Validando conversão
    assert dtype_pre_casting == StringType()
    assert dtype_pos_casting == DateType()


@pytest.mark.etl_manager
@pytest.mark.date_attributes_extraction
def test_conversao_de_timestamp_no_metodo_de_extracao_de_atributos_de_data(
    etl_manager, fake_dataframe, date_col="timestamp",
    date_col_type="timestamp", date_test_col_name="timestamp_test",
    date_format='%Y-%m-%d %H:%M:%S'
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método date_attributes_extraction() da classe
       GlueETLManager for executado em uma coluna de data com
       date_col_type="timestamp" e convert_string_to_date=True
    T: então o DataFrame resultante deve conter a mesma coluna de data
       porém com o tipo primitivo TimestampType()
    """

    # Aplicando casting forçado de campo de data para string
    fake_dataframe_cast = fake_dataframe.selectExpr(
        "*",
        f"cast({date_col} AS STRING) AS {date_test_col_name}"
    )

    # Executando método de extração de atributos de data
    fake_df_prep = etl_manager.date_attributes_extraction(
        df=fake_dataframe_cast,
        date_col=date_test_col_name,
        date_col_type=date_col_type,
        date_format=date_format,
        convert_string_to_date=True
    )

    # Extraindo informações antes da conversão
    dtype_pre_casting = fake_dataframe_cast\
        .schema[date_test_col_name].dataType

    # Extraindo tipo do campo após a conversão
    dtype_pos_casting = fake_df_prep\
        .schema[date_test_col_name].dataType

    # Validando conversão
    assert dtype_pre_casting == StringType()
    assert dtype_pos_casting == TimestampType()


@pytest.mark.etl_manager
@pytest.mark.date_attributes_extraction
def test_adicao_de_novas_colunas_apos_extracao_de_atributos_de_data(
    etl_manager, fake_dataframe, date_col="date"
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método date_attributes_extraction() da classe
       GlueETLManager for executado em uma coluna de data com os kwargs
       year=True, quarter=True, month=True, dayofmonth=True,
       dayofweak=True, dayofyear=True, weekofyear=True
    T: então o DataFrame resultante deverá conter uma coluna adicional
       para cada atributo de data extraído com os prefixos adequados
    """

    # Lista de possíveis atributos de data a serem extraídos
    possible_date_attribs = ["year", "quarter", "month", "dayofmonth",
                             "dayofweek", "dayofyear", "weekofyear"]

    # Gerando dicionário de kwargs para facilitar inserção no método
    kwargs_dict = {k: True for k in possible_date_attribs}

    # Executando método de extração de atributos de data
    df_date = etl_manager.date_attributes_extraction(
        df=fake_dataframe,
        date_col=date_col,
        convert_string_to_date=False,
        **kwargs_dict
    )

    # Criando lista de nomes de colunas para validação
    date_attribs_names = [f"{d}_{date_col}" for d in possible_date_attribs]

    # Validando presença de atributos de datas
    assert all(c in df_date.schema.fieldNames() for c in date_attribs_names)


@pytest.mark.etl_manager
@pytest.mark.date_attributes_extraction
def test_extracao_do_ano_de_atributo_de_data(
    etl_manager, fake_dataframe, date_col="date"
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método date_attributes_extraction() da classe
       GlueETLManager for executado em uma coluna de data com os kwargs
       year=True para extração do ano
    T: então o DataFrame resultante deverá conter uma coluna adicional
       trazendo o ano, de fato, da coluna de data alvo da análise
    """

    # Executando método de extração de atributos de data
    df_year = etl_manager.date_attributes_extraction(
        df=fake_dataframe,
        date_col=date_col,
        convert_string_to_date=False,
        year=True
    )

    # Extraindo lista esperada de anos para a coluna
    expected_years = [
        r[0].year for r in df_year.select(date_col).take(5)
    ]

    # Extraindo lista calculada de anos para a coluna
    calculated_years = [
        y[0] for y in df_year.select(f"year_{date_col}").take(5)
    ]

    # Validando igualdade das extrações
    assert calculated_years[:] == expected_years[:]


@pytest.mark.etl_manager
@pytest.mark.date_attributes_extraction
def test_extracao_do_mes_de_atributo_de_data(
    etl_manager, fake_dataframe, date_col="date"
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método date_attributes_extraction() da classe
       GlueETLManager for executado em uma coluna de data com os kwargs
       month=True para extração do mês
    T: então o DataFrame resultante deverá conter uma coluna adicional
       trazendo o mês, de fato, da coluna de data alvo da análise
    """

    # Executando método de extração de atributos de data
    df_year = etl_manager.date_attributes_extraction(
        df=fake_dataframe,
        date_col=date_col,
        convert_string_to_date=False,
        month=True
    )

    # Extraindo lista esperada de anos para a coluna
    expected_months = [
        r[0].month for r in df_year.select(date_col).take(5)
    ]

    # Extraindo lista calculada de anos para a coluna
    calculated_months = [
        y[0] for y in df_year.select(f"month_{date_col}").take(5)
    ]

    # Validando igualdade das extrações
    assert expected_months[:] == calculated_months[:]


@pytest.mark.etl_manager
@pytest.mark.date_attributes_extraction
def test_extracao_do_dia_de_atributo_de_data(
    etl_manager, fake_dataframe, date_col="date"
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método date_attributes_extraction() da classe
       GlueETLManager for executado em uma coluna de data com os kwargs
       month=True para extração do mês
    T: então o DataFrame resultante deverá conter uma coluna adicional
       trazendo o mês, de fato, da coluna de data alvo da análise
    """

    # Executando método de extração de atributos de data
    df_year = etl_manager.date_attributes_extraction(
        df=fake_dataframe,
        date_col=date_col,
        convert_string_to_date=False,
        dayofmonth=True
    )

    # Extraindo lista esperada de anos para a coluna
    expected_days = [
        r[0].day for r in df_year.select(date_col).take(5)
    ]

    # Extraindo lista calculada de anos para a coluna
    calculated_days = [
        y[0] for y in df_year.select(f"dayofmonth_{date_col}").take(5)
    ]

    # Validando igualdade das extrações
    assert expected_days[:] == calculated_days[:]


@pytest.mark.etl_manager
@pytest.mark.add_partition
def test_adicao_de_coluna_de_particao_anomesdia_dataframe(
    etl_manager, fake_dataframe, partition_name="anomesdia",
    partition_value=int(datetime.now().strftime("%Y%m%d"))
):
    """
    G: dado que o usuário deseja adicionar uma coluna de data
       para servir de partição de seu DataFrame Spark
    W: quando o usuário executar o método add_partition da classe
       GlueETLManager com os parâmetros partition_name="anomesdia"
       e partition_value=datetime.now().strftime("%Y%m%d")
    T: então o DataFrame resultante deve conter uma nova coluna
       de nome "anomesdia" do mesmo tipo primitivo do argumento
       partition_value
    """

    # Executando método de adição de partição em DataFrame
    df_partitioned = etl_manager.add_partition(
        df=fake_dataframe,
        partition_name=partition_name,
        partition_value=partition_value
    )

    # Coletando nome e valor de partição de novo DataFrame
    generated_partition_name = df_partitioned.schema[-1].name
    generated_partition_value = df_partitioned.selectExpr(
        partition_name
    ).take(1)[0][0]

    # Validando existência de nova coluna e seu valor
    assert generated_partition_name == partition_name
    assert generated_partition_value == partition_value


@pytest.mark.etl_manager
@pytest.mark.repartition_dataframe
def test_reparticionamento_de_dataframe_para_menos_particoes(
    etl_manager, fake_dataframe
):
    """
    G: dado que o usuário deseja reparticionar um DataFrame Spark
       para otimização do armazenamento físico do mesmo no s3
    W: quando o usuário executar o método repartition_dataframe()
       da classe GlueETLManager passando um número MENOR de
       partições físicas do que o número atual do DataFrame
    T: então o DataFrame resultante deverá conter o número
       especificado de partições
    """

    # Coletando informações sobre partições atuais do DataFrame
    current_partitions = fake_dataframe.rdd.getNumPartitions()
    partitions_to_set = current_partitions // 2

    # Repartitionando DataFrame
    df_repartitioned = etl_manager.repartition_dataframe(
        df=fake_dataframe,
        num_partitions=partitions_to_set
    )

    # Validando resultado
    assert df_repartitioned.rdd.getNumPartitions() == partitions_to_set


@pytest.mark.etl_manager
@pytest.mark.repartition_dataframe
def test_reparticionamento_de_dataframe_para_mais_particoes(
    etl_manager, fake_dataframe
):
    """
    G: dado que o usuário deseja reparticionar um DataFrame Spark
       para otimização do armazenamento físico do mesmo no s3
    W: quando o usuário executar o método repartition_dataframe()
       da classe GlueETLManager passando um número MAIOR de
       partições físicas do que o número atual do DataFrame
    T: então o DataFrame resultante deverá conter o número
       especificado de partições
    """

    # Coletando informações sobre partições atuais do DataFrame
    current_partitions = fake_dataframe.rdd.getNumPartitions()
    partitions_to_set = current_partitions * 2

    # Repartitionando DataFrame
    df_repartitioned = etl_manager.repartition_dataframe(
        df=fake_dataframe,
        num_partitions=partitions_to_set
    )

    # Validando resultado
    assert df_repartitioned.rdd.getNumPartitions() == partitions_to_set


"""@pytest.mark.etl_manager
@pytest.mark.generate_dynamicframe_dict
@mock_glue
def test_metodo_de_geracao_de_dynamicframes_gera_dicionario(
    client, create_fake_catalog_database, create_fake_catalog_table,
    etl_manager
):
    # Criando database e tabela fake no Data Catalog
    create_fake_catalog_database()
    create_fake_catalog_table()

    print(client.get_tables(DatabaseName="fakedb"))

    data_dict = {
        "fake_data": {
            "database": "fakedb",
            "table_name": "tbl_fake",
            "transformation_ctx": "dyf_orders",
            "create_temp_view": True
        }
    }


    assert False"""
