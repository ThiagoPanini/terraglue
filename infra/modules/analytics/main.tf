/* --------------------------------------------------
FILE: main.tf @ analytics module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: 

RESOURCES: Os recursos aqui implantados serão:
  - Databases no Glue Data Catalog
-------------------------------------------------- */

# Testando criação de databases
resource "aws_glue_catalog_database" "all" {
  for_each    = toset(var.glue_databases)
  name        = each.value
  description = "Database ${each.value} criado para simular schema de tabelas na criação de jobs do Glue"
}

# Testando a criação de tabelas
resource "aws_glue_catalog_table" "all" {
  for_each      = var.glue_catalog_map
  database_name = each.value.database
  name          = each.value.table_name
  description   = "Entrada para tabela ${each.value.database}.${each.value.table_name} contendo dados a serem utilizados em jobs do Glue"

  table_type = "EXTERNAL_TABLE"

  parameters = {
    "EXTERNAL"               = "TRUE"
    "skip.header.line.count" = "1"
  }

  storage_descriptor {
    location      = each.value.location
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      name                  = "csv_stream"
      serialization_library = "org.apache.hadoop.hive.serde2.OpenCSVSerde"

      parameters = {
        "separatorChar" = ","
        "quoteChar"     = "\"",
        "escapeChar"    = "\\"
      }
    }

    columns {
      name = each.value.columns[0]
    }

  }

  depends_on = [
    aws_glue_catalog_database.all
  ]
}
