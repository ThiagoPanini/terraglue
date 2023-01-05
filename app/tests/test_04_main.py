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
from pytest import mark
from pyspark.sql.types import StructType, StructField,\
    StringType, IntegerType, DateType, TimestampType,\
    LongType, DecimalType


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
       amostra contendo 10 registros de pedidos
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
@mark.order_items
def test_qtd_linhas_resultantes_pos_transformacao_order_items(
    df_order_items_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_order_items
    W: quando o usuário executar o método transform_order_items()
       da classe GlueTransformationManager utilizando uma
       amostra contendo 14 registros de itens pedidos
    T: então o DataFrame resultante deve retornar uma base
       agrupada contendo 10 registros
    """
    assert df_order_items_prep.count() == 10


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
@mark.customers
def test_qtd_linhas_resultantes_pos_transformacao_customers(
    df_customers, df_customers_prep
):
    """
    G: dado que o usuário deseja transformar dados presentes
       no DataFrame df_customers
    W: quando o usuário executar o método transform_customers()
       da classe GlueTransformationManager utilizando uma
       amostra contendo 10 registros de pedidos
    T: então o DataFrame resultante deve manter a granularidade
       e conter a mesma quantidade de 10 registros
    """
    assert df_customers_prep.count() == df_customers.count()


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
