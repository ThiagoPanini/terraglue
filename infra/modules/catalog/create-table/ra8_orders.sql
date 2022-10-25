CREATE EXTERNAL TABLE ra8.orders (
	order_id STRING,
	customer_id STRING,
	order_status STRING,
	order_purchase_timestamp STRING,
	order_approved_at STRING,
	order_delivered_carrier_date STRING,
	order_delivered_customer_date STRING,
	order_estimated_delivery_date STRING
)
COMMENT "Tabela criada para fins de validação e testes"
ROW FORMAT DELIMITED
	FIELDS TERMINATED BY ","
	LINES TERMINATED BY "\n"
STORED AS TEXTFILE
LOCATION "s3://<bucket_name>/ra8/orders"
TBLPROPERTIES ("skip.header.line.count"="1")