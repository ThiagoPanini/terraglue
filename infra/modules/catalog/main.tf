/* --------------------------------------------------
FILE: main.tf @ catalog module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: Este módulo tem por objetivo consolidar todas
as implantações relacionadas ao universo de catalogação
do projeto, incluindo os insumos e recursos necessários
para a execução completa de um job do glue contando
com uma simulação fidedigna de um data lake com
dados armazenados no s3 e entradas para o catálogo
de dados devidamente registrada de acordo com os 
arquivos presentes.

RESOURCES: Os recursos aqui implantados serão:
  - Databases no glue data catalog
  - Tabelas pré configuradas no glue data catalog
  - Workgroup no athena
-------------------------------------------------- */

# Criando databases no catálogo de dados
resource "aws_glue_catalog_database" "all" {
  for_each    = toset(var.glue_databases)
  name        = each.value
  description = "Database ${each.value} criado para simular schema de tabelas na criação de jobs do Glue"
}

# Criando tabelas em seus respectivos databases no catálogo
resource "aws_glue_catalog_table" "all" {
  for_each      = var.glue_catalog_map
  database_name = each.value.database
  name          = each.value.table_name
  description   = "Entrada para tabela ${each.value.database}.${each.value.table_name} contendo dados a serem utilizados em jobs do Glue"

  table_type = "EXTERNAL_TABLE"

  parameters = var.catalog_table_parameters

  storage_descriptor {
    location      = each.value.location
    input_format  = var.catalog_table_input_format
    output_format = var.catalog_table_output_format

    ser_de_info {
      name                  = "main-stream"
      serialization_library = var.catalog_table_serialization_library
      parameters            = var.catalog_table_ser_de_parameters
    }

    # Bloco dinâmico para iterar sobre a lista de atributos de cada tabela
    dynamic "columns" {
      for_each = each.value.columns
      content {
        name = columns.value
        type = "string"
      }
    }
  }

  depends_on = [
    aws_glue_catalog_database.all
  ]
}

# Coletando chave kms para volume ebs
data "aws_kms_key" "s3" {
  key_id = var.s3_kms_key_alias
}

# Criando workgroup para o Athena
resource "aws_athena_workgroup" "analytics" {
  count = var.flag_create_athena_workgroup ? 1 : 0

  name          = var.athena_workgroup_name
  force_destroy = true

  configuration {
    result_configuration {
      output_location = var.athena_workgroup_output_location

      encryption_configuration {
        encryption_option = "SSE_KMS"
        kms_key_arn       = data.aws_kms_key.s3.arn
      }
    }
  }
}
