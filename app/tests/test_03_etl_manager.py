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
from pytest import mark
from datetime import datetime
from pyspark.sql.types import StringType, DateType,\
   TimestampType, IntegerType


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


@mark.etl_manager
@mark.date_attributes_extraction
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


@mark.etl_manager
@mark.date_attributes_extraction
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


@mark.etl_manager
@mark.date_attributes_extraction
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


@mark.etl_manager
@mark.date_attributes_extraction
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
    assert calculated_years == expected_years


@mark.etl_manager
@mark.date_attributes_extraction
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
    assert expected_months == calculated_months


@mark.etl_manager
@mark.date_attributes_extraction
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
    assert expected_days == calculated_days
