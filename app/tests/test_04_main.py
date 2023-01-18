"""
SCRIPT: test_main.py

CONTEXTO:
---------
Script de testes criado para validar etapas de transformação
existentes no script principal da aplicação Spark
responsável por consolidar toda a aplicação de regras
de negócio utilizadas para o alcance dos objetivos
estabelecidos.

OBJETIVO:
---------
Consoldar uma suíte de testes capaz de testar e validar
todas as regras de negócio da aplicação materializadas
como métodos de transformação no script principal.
------------------------------------------------------

------------------------------------------------------
---------- 1. PREPARAÇÃO INICIAL DO SCRIPT -----------
          1.1 Importação das bibliotecas
---------------------------------------------------"""

# Importando módulos para uso
import pytest
from pytest import mark
from pyspark.sql.types import StructType, StructField,\
    StringType, IntegerType, DateType, TimestampType,\
    LongType, DecimalType, DoubleType


"""---------------------------------------------------
------------ 2. DEFININDO SUÍTE DE TESTES ------------
           2.1 Construindo testes unitários
---------------------------------------------------"""


@mark.main
@mark.orders
def test_qtd_linhas_resultantes_pos_transformacao_orders(
    df_orders, df_orders_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_orders
    W: quando o usuário executar o método transform_orders()
       da classe GlueTransformationManager utilizando uma
       amostra contendo 10 registros
    T: então o DataFrame resultante deve manter a granularidade
       e conter a mesma quantidade de 10 registros
    """
    assert df_orders_prep.count() == df_orders.count()


@mark.main
@mark.orders
def test_schema_resultante_pos_transformacao_orders(
    df_orders_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_orders
    W: quando o usuário executar o método transform_orders()
       da classe GlueTransformationManager
    T: então o DataFrame resultante deve conter um conjunto
       esperado de atributos e tipos primitivos
    """

    # Schema esperado
    expected_schema = StructType([
        StructField("order_id", StringType()),
        StructField("customer_id", StringType()),
        StructField("order_status", StringType()),
        StructField("order_purchase_timestamp", TimestampType()),
        StructField("order_approved_at", TimestampType()),
        StructField("order_delivered_carrier_date", TimestampType()),
        StructField("order_delivered_customer_date", TimestampType()),
        StructField("order_estimated_delivery_date", DateType()),
        StructField("year_order_purchase_timestamp", IntegerType()),
        StructField("quarter_order_purchase_timestamp", IntegerType()),
        StructField("month_order_purchase_timestamp", IntegerType()),
        StructField("dayofmonth_order_purchase_timestamp", IntegerType()),
        StructField("dayofweek_order_purchase_timestamp", IntegerType()),
        StructField("dayofyear_order_purchase_timestamp", IntegerType()),
        StructField("weekofyear_order_purchase_timestamp", IntegerType())
    ])

    assert df_orders_prep.schema == expected_schema


@mark.main
@mark.orders
def test_erro_criacao_de_dag_transformacao_orders(
    glue_manager, empty_df
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_orders (este estando vazio)
    W: quando o usuário executar o método transform_orders()
       da classe GlueTransformationManager utilizando um
       DataFrame vazio como argumento
    T: então o método deve retornar uma exceção por não
       conseguir preparar a DAG de transformações codificada
    """
    
    # Testando exceção
    with pytest.raises(Exception) as e_info:
        df_prep = glue_manager.transform_orders(empty_df)
    

@mark.main
@mark.order_items
def test_qtd_linhas_resultantes_pos_transformacao_order_items(
    df_order_items_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_order_items
    W: quando o usuário executar o método transform_order_items()
       da classe GlueTransformationManager utilizando uma
       amostra contendo 14 registros
    T: então o DataFrame resultante deve retornar uma base
       agrupada contendo 10 registros
    """
    assert df_order_items_prep.count() == 10


@mark.main
@mark.order_items
def test_nao_duplicidade_de_order_id_pos_transformacao_order_items(
    df_order_items_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_order_items
    W: quando o usuário executar o método transform_order_items()
       da classe GlueTransformationManager
    T: então não deve haver nenhum tipo de duplicidade pela chave
       order_id no DataFrame resultante
    """

    lines = df_order_items_prep.count()
    lines_distinct = df_order_items_prep\
        .dropDuplicates(subset=["order_id"]).count()

    assert lines_distinct == lines


@mark.main
@mark.order_items
def test_schema_resultante_pos_transformacao_order_items(
    df_order_items_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_order_items
    W: quando o usuário executar o método transform_order_items()
       da classe GlueTransformationManager
    T: então o DataFrame resultante deve conter um conjunto
       esperado de atributos e tipos primitivos
    """

    # Schema esperado
    expected_schema = StructType([
        StructField("order_id", StringType()),
        StructField("qty_order_items", LongType(), False),
        StructField("sum_price_order", DecimalType(17, 2)),
        StructField("avg_price_order", DecimalType(17, 2)),
        StructField("min_price_order_item", DecimalType(17, 2)),
        StructField("max_price_order_item", DecimalType(17, 2)),
        StructField("avg_freight_value_order", DecimalType(17, 2)),
        StructField("max_order_shipping_limit_date", TimestampType()),
    ])

    assert df_order_items_prep.schema == expected_schema


@mark.main
@mark.order_items
def test_erro_criacao_de_dag_transformacao_order_items(
    glue_manager, empty_df
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_order_items (este estando vazio)
    W: quando o usuário executar o método transform_order_items()
       da classe GlueTransformationManager utilizando um
       DataFrame vazio como argumento
    T: então o método deve retornar uma exceção por não
       conseguir preparar a DAG de transformações codificada
    """
    
    # Testando exceção
    with pytest.raises(Exception) as e_info:
        df_prep = glue_manager.transform_order_items(empty_df)


@mark.main
@mark.customers
def test_qtd_linhas_resultantes_pos_transformacao_customers(
    df_customers, df_customers_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_customers
    W: quando o usuário executar o método transform_customers()
       da classe GlueTransformationManager utilizando uma
       amostra contendo 10 registros
    T: então o DataFrame resultante deve manter a granularidade
       e conter a mesma quantidade de 10 registros
    """
    assert df_customers_prep.count() == df_customers.count()


@mark.main
@mark.customers
def test_nao_duplicidade_de_customer_id_pos_transformacao_customers(
    df_customers_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_customers
    W: quando o usuário executar o método transform_customers()
       da classe GlueTransformationManager
    T: então não deve haver nenhum tipo de duplicidade pela chave
       customer_id no DataFrame resultante
    """

    lines = df_customers_prep.count()
    lines_distinct = df_customers_prep\
        .dropDuplicates(subset=["customer_id"]).count()

    assert lines_distinct == lines


@mark.main
@mark.customers
def test_schema_resultante_pos_transformacao_customers(
    df_customers_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_customers
    W: quando o usuário executar o método transform_customers()
       da classe GlueTransformationManager
    T: então o DataFrame resultante deve conter um conjunto
       esperado de atributos e tipos primitivos
    """

    # Schema esperado
    expected_schema = StructType([
        StructField("customer_id", StringType()),
        StructField("customer_city", StringType()),
        StructField("customer_state", StringType())
    ])

    assert df_customers_prep.schema == expected_schema


@mark.main
@mark.customers
def test_erro_criacao_de_dag_transformacao_customers(
    glue_manager, empty_df
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_customers (este estando vazio)
    W: quando o usuário executar o método transform_customers()
       da classe GlueTransformationManager utilizando um
       DataFrame vazio como argumento
    T: então o método deve retornar uma exceção por não
       conseguir preparar a DAG de transformações codificada
    """
    
    # Testando exceção
    with pytest.raises(Exception) as e_info:
        df_prep = glue_manager.transform_customers(empty_df)


@mark.main
@mark.payments
def test_qtd_linhas_resultantes_pos_transformacao_payments(
    df_payments_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_payments
    W: quando o usuário executar o método transform_payments()
       da classe GlueTransformationManager utilizando uma
       amostra contendo 10 registros
    T: então o DataFrame resultante deve retornar uma base
       agrupada contendo 10 registros
    """
    assert df_payments_prep.count() == 10


@mark.main
@mark.payments
def test_nao_duplicidade_de_order_id_pos_transformacao_payments(
    df_payments_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_payments
    W: quando o usuário executar o método transform_payments()
       da classe GlueTransformationManager
    T: então não deve haver nenhum tipo de duplicidade pela chave
       order_id no DataFrame resultante
    """

    lines = df_payments_prep.count()
    lines_distinct = df_payments_prep\
        .dropDuplicates(subset=["order_id"]).count()

    assert lines_distinct == lines


@mark.main
@mark.payments
def test_schema_resultante_pos_transformacao_payments(
    df_payments_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_payments
    W: quando o usuário executar o método transform_customers()
       da classe GlueTransformationManager
    T: então o DataFrame resultante deve conter um conjunto
       esperado de atributos e tipos primitivos
    """

    # Schema esperado
    expected_schema = StructType([
        StructField("order_id", StringType()),
        StructField("installments", LongType(), False),
        StructField("sum_payments", DoubleType()),
        StructField("avg_payment_value", DoubleType()),
        StructField("distinct_payment_types", LongType(), False),
        StructField("most_common_payment_type", StringType())
    ])

    assert df_payments_prep.schema == expected_schema


@mark.main
@mark.payments
def test_erro_criacao_de_dag_transformacao_payments(
    glue_manager, empty_df
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_payments (este estando vazio)
    W: quando o usuário executar o método transform_payments()
       da classe GlueTransformationManager utilizando um
       DataFrame vazio como argumento
    T: então o método deve retornar uma exceção por não
       conseguir preparar a DAG de transformações codificada
    """
    
    # Testando exceção
    with pytest.raises(Exception) as e_info:
        df_prep = glue_manager.transform_payments(empty_df)


@mark.main
@mark.reviews
def test_qtd_linhas_resultantes_pos_transformacao_reviews(
    df_reviews_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_reviews
    W: quando o usuário executar o método transform_reviews()
       da classe GlueTransformationManager utilizando uma
       amostra contendo 10 registros
    T: então o DataFrame resultante deve retornar uma base
       agrupada contendo 10 registros
    """
    assert df_reviews_prep.count() == 10


@mark.main
@mark.reviews
def test_nao_duplicidade_de_order_id_pos_transformacao_reviews(
    df_reviews_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_reviews
    W: quando o usuário executar o método transform_reviews()
       da classe GlueTransformationManager
    T: então não deve haver nenhum tipo de duplicidade pela chave
       order_id no DataFrame resultante
    """

    lines = df_reviews_prep.count()
    lines_distinct = df_reviews_prep\
        .dropDuplicates(subset=["order_id"]).count()

    assert lines_distinct == lines


@mark.main
@mark.reviews
def test_schema_resultante_pos_transformacao_reviews(
    df_reviews_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_payments
    W: quando o usuário executar o método transform_customers()
       da classe GlueTransformationManager
    T: então o DataFrame resultante deve conter um conjunto
       esperado de atributos e tipos primitivos
    """

    # Schema esperado
    expected_schema = StructType([
        StructField("order_id", StringType()),
        StructField("review_best_score", IntegerType()),
        StructField("review_comment_message", StringType())
    ])

    assert df_reviews_prep.schema == expected_schema


@mark.main
@mark.reviews
def test_erro_criacao_de_dag_transformacao_reviews(
    glue_manager, empty_df
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_reviews (este estando vazio)
    W: quando o usuário executar o método transform_reviews()
       da classe GlueTransformationManager utilizando um
       DataFrame vazio como argumento
    T: então o método deve retornar uma exceção por não
       conseguir preparar a DAG de transformações codificada
    """
    
    # Testando exceção
    with pytest.raises(Exception) as e_info:
        df_prep = glue_manager.transform_reviews(empty_df)


@mark.main
@mark.sot
def test_qtd_linhas_resultantes_pos_transformacao_sot(
    df_sot_prep
):
    """
    G: dado que o usuário deseja obter a transformação final
       após as transformações individuais de suas roigens
    W: quando o usuário executar o método transform_sot()
       da classe GlueTransformationManager utilizando uma
       amostra contendo 10 registros
    T: então o DataFrame resultante deve retornar uma base
       agrupada contendo 10 registros
    """
    assert df_sot_prep.count() == 10


@mark.main
@mark.sot
def test_nao_duplicidade_de_order_id_pos_transformacao_sot(
    df_sot_prep
):
    """
    G: dado que o usuário deseja obter a transformação final
       após as transformações individuais de suas roigens
    W: quando o usuário executar o método transform_sot()
       da classe GlueTransformationManager
    T: então não deve haver nenhum tipo de duplicidade pela chave
       order_id no DataFrame resultante
    """

    lines = df_sot_prep.count()
    lines_distinct = df_sot_prep\
        .dropDuplicates(subset=["order_id"]).count()

    assert lines_distinct == lines


@mark.main
@mark.sot
def test_schema_resultante_pos_transformacao_sot(
    df_sot_prep
):
    """
    G: dado que o usuário deseja obter a transformação final
       após as transformações individuais de suas roigens
    W: quando o usuário executar o método transform_sot()
       da classe GlueTransformationManager
    T: então o DataFrame resultante deve conter um conjunto
       esperado de atributos e tipos primitivos
    """

    # Schema esperado
    expected_schema = StructType([
        StructField("order_id", StringType()),
        StructField("customer_id", StringType()),
        StructField("order_status", StringType()),
        StructField("order_purchase_timestamp", TimestampType()),
        StructField("order_approved_at", TimestampType()),
        StructField("order_delivered_carrier_date", TimestampType()),
        StructField("order_delivered_customer_date", TimestampType()),
        StructField("order_estimated_delivery_date", DateType()),
        StructField("year_order_purchase_timestamp", IntegerType()),
        StructField("quarter_order_purchase_timestamp", IntegerType()),
        StructField("month_order_purchase_timestamp", IntegerType()),
        StructField("dayofmonth_order_purchase_timestamp", IntegerType()),
        StructField("dayofweek_order_purchase_timestamp", IntegerType()),
        StructField("dayofyear_order_purchase_timestamp", IntegerType()),
        StructField("weekofyear_order_purchase_timestamp", IntegerType()),
        StructField("qty_order_items", LongType(), False),
        StructField("sum_price_order", DecimalType(17, 2)),
        StructField("avg_price_order", DecimalType(17, 2)),
        StructField("min_price_order_item", DecimalType(17, 2)),
        StructField("max_price_order_item", DecimalType(17, 2)),
        StructField("avg_freight_value_order", DecimalType(17, 2)),
        StructField("max_order_shipping_limit_date", TimestampType()),
        StructField("customer_city", StringType()),
        StructField("customer_state", StringType()),
        StructField("installments", LongType()),
        StructField("sum_payments", DoubleType()),
        StructField("avg_payment_value", DoubleType()),
        StructField("distinct_payment_types", LongType()),
        StructField("most_common_payment_type", StringType()),
        StructField("review_best_score", IntegerType()),
        StructField("review_comment_message", StringType())
    ])

    df_sot_prep.printSchema()

    assert df_sot_prep.schema == expected_schema


@mark.main
@mark.sot
def test_erro_criacao_de_dag_transformacao_sot(
    glue_manager, empty_df
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_sot (este estando vazio)
    W: quando o usuário executar o método transform_sot()
       da classe GlueTransformationManager utilizando um
       DataFrame vazio como argumento
    T: então o método deve retornar uma exceção por não
       conseguir preparar a DAG de transformações codificada
    """
    
    # Testando exceção
    with pytest.raises(Exception) as e_info:
        df_prep = glue_manager.transform_sot(empty_df)
