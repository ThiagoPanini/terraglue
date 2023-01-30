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

import pytest
from datetime import datetime
import copy

from pyspark.sql.types import StringType, DateType, TimestampType
from pyspark.sql import DataFrame

from awsglue.dynamicframe import DynamicFrame


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


@pytest.mark.etl_manager
@pytest.mark.generate_dynamicframe_dict
def test_metodo_de_geracao_de_dynamicframes_gera_dicionario(
    dyf_dict
):
    """
    G: dado que o usuário deseja realizar a leitura de dynamicframes
       com base na variável DATA_DICT devidamente definida
    W: quando o método generate_dynamic_frames_dict() for executado
    T: então o objeto resultante deve ser um dicionário
    """
    assert type(dyf_dict) == dict


@pytest.mark.etl_manager
@pytest.mark.generate_dynamicframe_dict
def test_dict_de_dyfs_possui_qtd_de_elementos_iguais_ao_dict_datadict(
    dyf_dict, data_dict
):
    """
    G: dado que o usuário deseja realizar a leitura de dynamicframes
       com base na variável DATA_DICT devidamente definida
    W: quando o método generate_dynamic_frames_dict() for executado
    T: então a quantidade de elementos presente no dicionário de
       dynamicframes resultante precisa ser igual à quantidade de
       elementos do dicionário DATA_DICT
    """
    assert len(dyf_dict) == len(data_dict)


@pytest.mark.etl_manager
@pytest.mark.generate_dynamicframe_dict
def test_tipo_primitivo_dos_elementos_do_dicionario_de_dynamicframes(
    dyf_dict
):
    """
    G: dado que o usuário deseja realizar a leitura de dynamicframes
       com base na variável DATA_DICT devidamente definida
    W: quando o método generate_dynamic_frames_dict() for executado
    T: então os elementos que compõem o dicionário resultante precisam
       ser do tipo DynamicFrame do Glue
    """
    # Extraindo lista de tipos primitivos
    dyfs = list(dyf_dict.values())
    assert all(type(dyf) == DynamicFrame for dyf in dyfs)


@pytest.mark.etl_manager
@pytest.mark.generate_dynamicframe_dict
def test_erro_ao_gerar_dynamicframes_de_tabelas_inexistentes_no_catalogo(
    etl_manager
):
    """
    G: dado que o usuário deseja realizar a leitura de dynamicframes
       com base na variável DATA_DICT devidamente definida
    W: quando o método generate_dynamic_frames_dict() for executado com
       alguma inconsistência na definição da variável DATA_DICT que
       indique a leitura de tabelas inexistentes no catálogo de dados ou
       com alguma restrição de acesso do usuário
    T: então uma exceção deve ser lançada
    """
    # Copiando objeto
    etl_manager_copy = copy.deepcopy(etl_manager)

    # Modificando atributo data_dict
    data_dict_copy = etl_manager_copy.data_dict
    data_dict_copy[list(data_dict_copy.keys())[0]]["database"] \
        = "a fake database"

    # Assimilando DATA_DICT modificado ao objeto da classe
    etl_manager_copy.data_dict = data_dict_copy
    etl_manager_copy.init_job()

    # Executando método de geração de DynamicFrames
    with pytest.raises(Exception):
        _ = etl_manager_copy.generate_dynamic_frames_dict()


@pytest.mark.etl_manager
@pytest.mark.generate_dataframe_dict
def test_metodo_de_geracao_de_dataframes_gera_dicionario(
    df_dict
):
    """
    G: dado que o usuário deseja realizar a leitura de dataframes
       com base na variável DATA_DICT devidamente definida
    W: quando o método generate_dataframes_dict() for executado
    T: então o objeto resultante deve ser um dicionário
    """
    assert type(df_dict) == dict


@pytest.mark.etl_manager
@pytest.mark.generate_dataframe_dict
def test_dict_de_dfs_possui_qtd_de_elementos_iguais_ao_dict_datadict(
    df_dict, data_dict
):
    """
    G: dado que o usuário deseja realizar a leitura de dataframes
       com base na variável DATA_DICT devidamente definida
    W: quando o método generate_dataframes_dict() for executado
    T: então a quantidade de elementos presente no dicionário de
       dataframes resultante precisa ser igual à quantidade de
       elementos do dicionário DATA_DICT
    """
    assert len(df_dict) == len(data_dict)


@pytest.mark.etl_manager
@pytest.mark.generate_dataframe_dict
def test_tipo_primitivo_dos_elementos_do_dicionario_de_dataframes(
    df_dict
):
    """
    G: dado que o usuário deseja realizar a leitura de dataframes
       com base na variável DATA_DICT devidamente definida
    W: quando o método generate_dataframes_dict() for executado
    T: então os elementos que compõem o dicionário resultante precisam
       ser do tipo DataFrame do Spark
    """
    # Extraindo lista de tipos primitivos
    dfs = list(df_dict.values())
    assert all(type(df) == DataFrame for df in dfs)


@pytest.mark.etl_manager
@pytest.mark.extract_date_attributes
def test_conversao_de_data_no_metodo_de_extracao_de_atributos_de_data(
    etl_manager, fake_dataframe, date_col="date", date_col_type="date",
    date_test_col_name="date_test", date_format='%Y-%m-%d'
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método extract_date_attributes() da classe
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
    fake_df_prep = etl_manager.extract_date_attributes(
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
@pytest.mark.extract_date_attributes
def test_conversao_de_timestamp_no_metodo_de_extracao_de_atributos_de_data(
    etl_manager, fake_dataframe, date_col="timestamp",
    date_col_type="timestamp", date_test_col_name="timestamp_test",
    date_format='%Y-%m-%d %H:%M:%S'
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método extract_date_attributes() da classe
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
    fake_df_prep = etl_manager.extract_date_attributes(
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
@pytest.mark.extract_date_attributes
def test_adicao_de_novas_colunas_apos_extracao_de_atributos_de_data(
    etl_manager, fake_dataframe, date_col="date"
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método extract_date_attributes() da classe
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
    df_date = etl_manager.extract_date_attributes(
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
@pytest.mark.extract_date_attributes
def test_extracao_do_ano_de_atributo_de_data(
    etl_manager, fake_dataframe, date_col="date"
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método extract_date_attributes() da classe
       GlueETLManager for executado em uma coluna de data com os kwargs
       year=True para extração do ano
    T: então o DataFrame resultante deverá conter uma coluna adicional
       trazendo o ano, de fato, da coluna de data alvo da análise
    """

    # Executando método de extração de atributos de data
    df_year = etl_manager.extract_date_attributes(
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
@pytest.mark.extract_date_attributes
def test_extracao_do_mes_de_atributo_de_data(
    etl_manager, fake_dataframe, date_col="date"
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método extract_date_attributes() da classe
       GlueETLManager for executado em uma coluna de data com os kwargs
       month=True para extração do mês
    T: então o DataFrame resultante deverá conter uma coluna adicional
       trazendo o mês, de fato, da coluna de data alvo da análise
    """

    # Executando método de extração de atributos de data
    df_year = etl_manager.extract_date_attributes(
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
@pytest.mark.extract_date_attributes
def test_extracao_do_dia_de_atributo_de_data(
    etl_manager, fake_dataframe, date_col="date"
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método extract_date_attributes() da classe
       GlueETLManager for executado em uma coluna de data com os kwargs
       month=True para extração do mês
    T: então o DataFrame resultante deverá conter uma coluna adicional
       trazendo o mês, de fato, da coluna de data alvo da análise
    """

    # Executando método de extração de atributos de data
    df_year = etl_manager.extract_date_attributes(
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
@pytest.mark.extract_date_attributes
def test_erro_ao_fornecer_argumento_date_col_type_incorreto(
    etl_manager, fake_dataframe, date_col="date"
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método extract_date_attributes() da classe
       GlueETLManager for executado em uma coluna de data com o
       argumento date_col_type não configurado como 'date' ou 'timestamp'
    T: então uma exceção deve ser lançada
    """
    with pytest.raises(Exception):
        _ = etl_manager.extract_date_attributes(
            df=fake_dataframe,
            date_col=date_col,
            convert_string_to_date=True,
            date_col_type="string"
        )


@pytest.mark.etl_manager
@pytest.mark.extract_date_attributes
def test_erro_ao_extrair_atributos_de_data_em_coluna_nao_compativel(
    etl_manager, fake_dataframe, date_col="bool"
):
    """
    G: dado que o usuário deseja aplicar o método de extração de
       atributos de data em uma operação de transformação de dados
    W: quando o método método extract_date_attributes() da classe
       GlueETLManager for executado em uma coluna não compatível ou
       não transformável em data e com o flag convert_string_to_date
       igual a True
    T: então uma exceção deve ser lançada
    """
    with pytest.raises(Exception):
        _ = etl_manager.extract_date_attributes(
            df=fake_dataframe,
            date_col=date_col,
            convert_string_to_date=True,
            date_col_type="date"
        )


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
@pytest.mark.add_partition
def test_erro_ao_adicionar_particao_com_nome_de_particao_invalido(
    etl_manager, fake_dataframe, partition_name=None,
    partition_value="1"
):
    """
    G: dado que o usuário deseja adicionar uma coluna de data
       para servir de partição de seu DataFrame Spark
    W: quando o usuário executar o método add_partition da classe
       GlueETLManager com o argumento partition_name igual a None
    T: então uma exceção deve ser lançada
    """
    with pytest.raises(Exception):
        _ = etl_manager.add_partition(
            df=fake_dataframe,
            partition_name=partition_name,
            partition_value=partition_value
        )


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


@pytest.mark.etl_manager
@pytest.mark.repartition_dataframe
def test_reparticionamento_de_dataframe_para_mesmo_numero_de_particoes(
    etl_manager, fake_dataframe
):
    """
    G: dado que o usuário deseja reparticionar um DataFrame Spark
       para otimização do armazenamento físico do mesmo no s3
    W: quando o usuário executar o método repartition_dataframe()
       da classe GlueETLManager passando um número IGUAL de
       partições físicas do que o número atual do DataFrame
    T: então nenhuma operação deve ser realizada e o mesmo DataFrame
       passado como input deve ser retornado com o número de
       partições intacto
    """
    # Coletando informações sobre partições atuais do DataFrame
    current_partitions = fake_dataframe.rdd.getNumPartitions()
    partitions_to_set = current_partitions

    # Repartitionando DataFrame
    df_repartitioned = etl_manager.repartition_dataframe(
        df=fake_dataframe,
        num_partitions=partitions_to_set
    )

    # Validando resultado
    assert df_repartitioned.rdd.getNumPartitions() == partitions_to_set


@pytest.mark.etl_manager
@pytest.mark.repartition_dataframe
def test_erro_ao_repartitionar_dataframe_com_numero_invalido_de_particoes(
    etl_manager, fake_dataframe, partitions_to_set=-1
):
    """
    G: dado que o usuário deseja reparticionar um DataFrame Spark
       para otimização do armazenamento físico do mesmo no s3
    W: quando o usuário executar o método repartition_dataframe()
       da classe GlueETLManager passando um número negativo de
       partições
    T: então nenhuma operação deve ser realizada e o mesmo DataFrame
       passado como input deve ser retornado com o número de
       partições intacto
    """
    # Coletando informações sobre partições atuais do DataFrame
    current_partitions = fake_dataframe.rdd.getNumPartitions()

    # Repartitionando DataFrame
    df_repartitioned = etl_manager.repartition_dataframe(
        df=fake_dataframe,
        num_partitions=partitions_to_set
    )

    # Validando resultado
    assert df_repartitioned.rdd.getNumPartitions() == current_partitions


@pytest.mark.etl_manager
@pytest.mark.extract_aggregate_statistics
def test_extracao_de_estatisticas_gera_coluna_com_nomenclatura_adequada(
    spark, etl_manager, fake_dataframe, numeric_col="value", group_by="id"
):
    """
    G: dado que o usuário deseja extrair atributos estatísticos de um
       objeto do tipo DataFrame Spark
    W: quando o método extract_aggregate_statistics() for executado para
       a extração da soma de um atributo numérico (sum=True)
    T: então a coluna resultante deve seguir o padrão "sum_<coluna>"
    """
    # Inicializando job
    etl_manager.init_job()

    # Executando método
    df_prep = etl_manager.extract_aggregate_statistics(
        df=fake_dataframe,
        numeric_col=numeric_col,
        group_by=group_by,
        sum=True
    )

    # Extraindo coluna gerada
    assert df_prep.columns[-1] == f"sum_{numeric_col}"


@pytest.mark.etl_manager
@pytest.mark.extract_aggregate_statistics
def test_extracao_de_estatisticas_com_lista_de_colunas_no_groupby(
    spark, etl_manager, fake_dataframe, numeric_col="value",
    group_by=["id", "boolean"]
):
    """
    G: dado que o usuário deseja extrair atributos estatísticos de um
       objeto do tipo DataFrame Spark
    W: quando o método extract_aggregate_statistics() for executado com
       a definição de múltiplas colunas no parâmetro "group_by"
    T: então a agregação deve ser feita através destas múltiplas colunas
       e o DataFrame resultante deve conter tais colunas em seu resultado
    """
    # Inicializando job
    etl_manager.init_job()

    # Executando método
    df_prep = etl_manager.extract_aggregate_statistics(
        df=fake_dataframe,
        numeric_col=numeric_col,
        group_by=group_by,
        sum=True
    )

    # Verificando se colunas de agrupamento estão no DataFrame resultante
    assert all(col in df_prep.columns for col in group_by)


@pytest.mark.etl_manager
@pytest.mark.extract_aggregate_statistics
def test_erro_de_extracao_de_estatisticas_por_falta_de_parametrizacao(
    spark, etl_manager, fake_dataframe, numeric_col="value",
    group_by=["id", "boolean"]
):
    """
    G: dado que o usuário deseja extrair atributos estatísticos de um
       objeto do tipo DataFrame Spark
    W: quando o método extract_aggregate_statistics() for executado sem
       a definição de uma agregação estatística em seus **kwargfs
    T: então uma exceção deve ser lançada
    """
    # Inicializando job
    etl_manager.init_job()

    # Executando método sem nenhuma agregação estatística definida
    with pytest.raises(Exception):
        _ = etl_manager.extract_aggregate_statistics(
            df=fake_dataframe,
            numeric_col=numeric_col,
            group_by=group_by,
        )
