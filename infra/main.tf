/* --------------------------------------------------
FILE: main.tf @ root module

CONTEXT: Arquivo principal de construção da infra que,
através das informações contidas nos outros arquivos
.tf e nos módulos especificados em ./modules, realiza
a especificação dos elementos a serem implantados
nos providers declarados.

GOAL: 

MODULES: A organização da infra comporta os módulos:
  - ./modules/storage
  - ./modules/analytics

Especificações e detalhes sobre o conteúdo de cada
módulo poderá ser encontrado em seus respectivos
arquivos main.tf
-------------------------------------------------- */

# Definindo data sources para auxiliar na nomenclatura de variáveis
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}


/* --------------------------------------------------
------------- MÓDULO TERRAFORM: storage -------------
      Criando recursos de armazenamento na conta
-------------------------------------------------- */

# Definindo variáveis locais para uso no módulo
locals {
  bucket_names_map = {
    "sor"    = "sbx-sor-data-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
    "athena" = "sbx-athena-query-results-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
    "glue"   = "sbx-glue-scripts-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
  }
}

# Chamando módulo storage
module "storage" {
  source = "./modules/storage"

  bucket_names_map       = local.bucket_names_map
  local_data_path        = var.local_data_path
  flag_upload_data_files = var.flag_upload_data_files
}


/* --------------------------------------------------
------------ MÓDULO TERRAFORM: analytics ------------
      Recursos para consolidação de pipelines
-------------------------------------------------- */

# Variáveis locais para um melhor gerenciamento dos recursos do módulo
locals {
  # Coletando todos os arquivos presentes no diretório de dados
  data_files = fileset(var.local_data_path, "**")

  # Coletando databases e nomes de tabelas com base em diretórios
  db_names  = [for f in local.data_files : split("/", f)[0]]
  tbl_names = [for f in local.data_files : split("/", f)[1]]
  tbl_keys = [
    for i in range(length(local.db_names)) :
    "${local.db_names[i]}_${local.tbl_names[i]}"
  ]

  # Criando lista de headers de cada um dos arquivos
  file_headers = [
    for f in local.data_files : replace([
      for line in split("\n", file("${var.local_data_path}${f}")) :
      trimspace(line)
    ][0], "\"", "")
  ]

  # Criando estruturas para mapeamento dos tipos primitivos
  column_names = [for c in local.file_headers : split(",", lower(c))]

  # Criando lista de localizações dos arquivos físicos no s3
  s3_locations = [
    for i in range(length(local.data_files)) :
    "s3://${module.storage.bucket_name_sor}/${local.db_names[i]}/${local.tbl_names[i]}"
  ]

  # Gerando dicionário final com as informações necessárias
  glue_catalog_map = {
    for i in range(length(local.data_files)) :
    local.tbl_keys[i] => {
      "database"   = local.db_names[i]
      "table_name" = local.tbl_names[i]
      "location"   = local.s3_locations[i]
      "columns"    = local.column_names[i]
    }
  }
}

# Chamando módulo analytics
module "catalog" {
  source = "./modules/catalog"

  # Variáveis para criação de entradas no catálogo de dados
  glue_databases                      = local.db_names
  glue_catalog_map                    = local.glue_catalog_map
  catalog_table_parameters            = var.catalog_table_parameters
  catalog_table_input_format          = var.catalog_table_input_format
  catalog_table_output_format         = var.catalog_table_output_format
  catalog_table_serialization_library = var.catalog_table_serialization_library
  catalog_table_ser_de_parameters     = var.catalog_table_ser_de_parameters

  # Variáveis de configuração do athena para consultas nos dados
  flag_create_athena_workgroup     = var.flag_create_athena_workgroup
  athena_workgroup_name            = var.athena_workgroup_name
  athena_workgroup_output_location = "s3://${module.storage.bucket_name_athena}"
  s3_kms_key_alias                 = var.s3_kms_key_alias

  depends_on = [
    module.storage
  ]
}
