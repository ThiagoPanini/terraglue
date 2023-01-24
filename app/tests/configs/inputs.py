"""
SCRIPT: configs/inputs.py

CONTEXTO E OBJETIVO:
--------------------
Arquivo de configuração de parâmetros e variáveis
utilizadas nos testes. O usuário deve atentar-se a todas
as configurações e declarações de variáveis aqui
realizadas para que os testes unitários possam ser
executados de maneira adequada.
---------------------------------------------------"""

from pyspark.sql.types import StructType, StructField,\
    IntegerType, StringType, BooleanType, DecimalType,\
    DateType, TimestampType


"""---------------------------------------------------
------ 1. DEFININDO PARÂMETROS DE CONFIGURAÇÃO -------
    1.1 Argumentos do job e entradas do usuário
---------------------------------------------------"""

# Argumentos obrigatórios do job a serem validados
JOB_REQUIRED_ARGS = [
    "JOB_NAME",
    "OUTPUT_BUCKET",
    "OUTPUT_DB",
    "OUTPUT_TABLE",
    "CONNECTION_TYPE",
    "UPDATE_BEHAVIOR",
    "DATA_FORMAT",
    "COMPRESSION",
    "ENABLE_UPDATE_CATALOG"
]

# Nome da variável terraform onde os demais parâmetros são declarados
TF_VAR_NAME_JOB_ARGS = "glue_job_user_arguments"

# Lista de argumentos do job definidos em tempo de execução
JOB_RUNTIME_ARGS = ["JOB_NAME", "OUTPUT_BUCKET"]

# Lista de chaves obrigatórias da variável DATA_DICT em main.py
DATA_DICT_REQUIRED_KEYS = ["database", "table_name", "transformation_ctx"]


"""---------------------------------------------------
------ 2. DEFININDO PARÂMETROS DE CONFIGURAÇÃO -------
     2.2 Parâmetros para mock de DataFrame Spark
---------------------------------------------------"""

# Schema para criação de DataFrame fictício Spark
FAKE_DATAFRAME_SCHEMA = StructType([
    StructField("id", StringType()),
    StructField("value", IntegerType()),
    StructField("decimal", DecimalType()),
    StructField("boolean", BooleanType()),
    StructField("date", DateType()),
    StructField("timestamp", TimestampType())
])


"""---------------------------------------------------
------ 2. DEFININDO PARÂMETROS DE CONFIGURAÇÃO -------
       2.3 Parâmetros para mock no Data Catalog
---------------------------------------------------"""

# Input para mock de banco de dados
FAKE_CATALOG_DATABASE_INPUT = {
    "Name": "db_fake",
    "Description": "a fake database",
    "LocationUri": "s3://bucket-fake/db_fake",
    "Parameters": {},
    "CreateTableDefaultPermissions": [
        {
            "Principal": {"DataLakePrincipalIdentifier": "a_fake_owner"},
            "Permissions": ["ALL"],
        },
    ],
}

# Input para mock de tabelas no catálogo
FAKE_CATALOG_TABLE_INPUT = {
    "Name": "tbl_fake",
    "Description": "Entrada para tabela db_fake.tbl_fake contendo "
                   "metadados mockados para uso em testes unitários",
    "Retention": 0,
    "StorageDescriptor": {
        "Columns": [
            {
                "Name": "fake_col_1",
                "Type": "string",
                "Comment": "",
                "Parameters": {}
            },
            {
                "Name": "fake_col_2",
                "Type": "string",
                "Comment": "",
                "Parameters": {}
            },
            {
                "Name": "fake_col_3",
                "Type": "string",
                "Comment": "",
                "Parameters": {}
            },
            {
                "Name": "fake_col_4",
                "Type": "string",
                "Comment": "",
                "Parameters": {}
            },
            {
                "Name": "fake_col_5",
                "Type": "string",
                "Comment": "",
                "Parameters": {}
            }
        ],
        "Location": "s3://bucket-fake/db_fake/tbl_fake",
        "InputFormat": "org.apache.hadoop.hive.ql.io.parquet"
                       ".MapredParquetInputFormat",
        "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet."
                        "MapredParquetOutputFormat",
        "Compressed": False,
        "NumberOfBuckets": 0,
        "SerdeInfo": {
            "Name": "main-stream",
            "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet."
                                    "serde.ParquetHiveSerDe",
        },
        "BucketColumns": [],
        "SortColumns": [],
        "Parameters": {},
        "StoredAsSubDirectories": False
    },
    "PartitionKeys": [],
    "TableType": "EXTERNAL_TABLE",
    "Parameters": {
        "EXTERNAL": "TRUE"
    }
}

# Simulação de data_dict com recursos mockados
FAKE_DATA_DICT = {
    "fake": {
        "database": "db_fake",
        "table_name": "tbl_fake",
        "transformation_ctx": "dyf_fake",
        "create_temp_view": False
    }
}
