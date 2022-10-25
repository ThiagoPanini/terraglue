CREATE EXTERNAL TABLE ra8.products (
	product_id STRING,
	product_category_name STRING,
	product_name_lenght STRING,
	product_description_lenght STRING,
	product_photos_qty STRING,
	product_weight_g STRING,
	product_length_cm STRING,
	product_height_cm STRING,
	product_width_cm STRING
)
COMMENT "Tabela criada para fins de validação e testes"
ROW FORMAT DELIMITED
	FIELDS TERMINATED BY ","
	LINES TERMINATED BY "\n"
STORED AS TEXTFILE
LOCATION "s3://<bucket_name>/ra8/products"
TBLPROPERTIES ("skip.header.line.count"="1")