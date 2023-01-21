"""
MÓDULO: mock_helper.py

CONTEXTO:
---------
Módulo criado para facilitar algumas operações de mockagem
de estruturas do glue, como databases, tabelas e dados.

OBJETIVO:
---------
Proporcionar uma série de funcionalidades capazes de
facilitar a construção de testes unitários em situações
que envolvem o consumo de dados fictícios mockados
como tabelas no Data Catalog
-----------------------------------------------------

# Input para mock de banco de dados
DATABASE_INPUT = {
    "Name": "fakedb",
    "Description": "a fake database",
    "LocationUri": "s3://fake-bucket/fake-prefix",
    "Parameters": {},
    "CreateTableDefaultPermissions": [
        {
            "Principal": {"DataLakePrincipalIdentifier": "a_fake_owner"},
            "Permissions": ["ALL"],
        },
    ],
}

# Input para mock de tabelas no catálogo
TABLE_INPUT = {
    "Name": "tbl_fake",
    "Description": "a fake table",
    "Owner": "a_fake_owner",
    "Parameters": {"EXTERNAL": "TRUE"},
    "Retention": 0,
    "StorageDescriptor": {
        "BucketColumns": [],
        "Compressed": False,
        "InputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat",
        "NumberOfBuckets": -1,
        "OutputFormat": "org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat",
        "Parameters": {},
        "SerdeInfo": {
            "Parameters": {"serialization.format": "1"},
            "SerializationLibrary": "org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe",
        },
        "SkewedInfo": {
            "SkewedColumnNames": [],
            "SkewedColumnValueLocationMaps": {},
            "SkewedColumnValues": [],
        },
        "SortColumns": [],
        "StoredAsSubDirectories": False,
    },
    "TableType": "EXTERNAL_TABLE",
}"""
