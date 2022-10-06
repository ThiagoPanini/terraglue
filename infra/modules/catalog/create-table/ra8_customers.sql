CREATE EXTERNAL TABLE ra8.customers (
	customer_id STRING,
	customer_unique_id STRING,
	customer_zip_code_prefix STRING,
	customer_city STRING,
	customer_state STRING
)
COMMENT "Tabela criada para fins de validação e testes"
ROW FORMAT DELIMITED
	FIELDS TERMINATED BY ","
	LINES TERMINATED BY "\n"
STORED AS TEXTFILE
LOCATION "s3://<bucket_name>/ra8/customers"
TBLPROPERTIES ("skip.header.line.count"="1")