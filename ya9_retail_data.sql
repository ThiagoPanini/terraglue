CREATE EXTERNAL TABLE ya9.retail_data (
	invoiceno STRING,
	stockcode STRING,
	description STRING,
	quantity STRING,
	invoicedate STRING,
	unitprice STRING,
	customerid STRING,
	country STRING
)
COMMENT "Tabela criada para fins de validação e testes"
ROW FORMAT DELIMITED
	FIELDS TERMINATED BY ","
	LINES TERMINATED BY "\n"
STORED AS TEXTFILE
LOCATION "s3://<bucket_name>/ya9/retail_data"
TBLPROPERTIES ("skip.header.line.count"="1")