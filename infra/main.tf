/* --------------------------------------------------
FILE: main.tf @ root module

CONTEXT: Arquivo principal de construção da infra que,
através das informações contidas nos outros arquivos
.tf e nos módulos especificados em ./modules, realiza
a especificação dos elementos a serem implantados
nos providers declarados.

GOAL: Consolidar as chamdas de todos os módulos utilizados
neste projeto de IaC para a completa implantação de um
ambiente analítico capaz de ser utilizado como uma rica
fonte de aprendizado para a criação de jobs do Glue.

MODULES: A organização da infra comporta os módulos:
  - ./modules/storage
  - ./modules/catalog
  - ./modules/iam
  - ./modules/glue

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
    "sor"    = "terraglue-sor-data-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
    "sot"    = "terraglue-sot-data-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
    "spec"   = "terraglue-spec-data-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
    "athena" = "terraglue-athena-query-results-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
    "glue"   = "terraglue-glue-assets-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
  }
}

# Chamando módulo storage
module "storage" {
  source = "./modules/storage"

  bucket_names_map            = local.bucket_names_map
  local_data_path             = var.local_data_path
  flag_upload_data_files      = var.flag_upload_data_files
  flag_s3_block_public_access = var.flag_s3_block_public_access
}


/* --------------------------------------------------
------------- MÓDULO TERRAFORM: catalog -------------
        Configurando e preparando o Data Catalog
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


/* --------------------------------------------------
--------------- MÓDULO TERRAFORM: iam ---------------
      Políticas e role de acessos de serviços
-------------------------------------------------- */

# Chamando módulo iam
module "iam" {
  source             = "./modules/iam"
  iam_policies_path  = var.iam_policies_path
  iam_glue_role_name = var.iam_glue_role_name
}


/* --------------------------------------------------
-------------- MÓDULO TERRAFORM: glue ---------------
      Definição e configuração de job do Glue
-------------------------------------------------- */

# Variáveis locais para um melhor gerenciamento dos recursos do módulo
# https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html
locals {
  # Coletando módulos Python extra a serem adicionados como arquivos extra no job
  glue_extra_py_files = join(",", [
    for f in setsubtract(fileset(var.glue_app_src_dir, "**.py"), [var.glue_script_file_name]) :
    "s3://${module.storage.bucket_name_glue}/jobs/${var.glue_job_name}/src/${f}"
  ])

  # Modificando dicionário de argumentos e incluindo referências de URIs do s3 para assets
  glue_job_dynamic_arguments = {
    "--scriptLocation"        = "s3://${local.bucket_names_map["glue"]}/scripts/"
    "--spark-event-logs-path" = "s3://${local.bucket_names_map["glue"]}/sparkHistoryLogs/"
    "--TempDir"               = "s3://${local.bucket_names_map["glue"]}/temporary/"
    "--OUTPUT_BUCKET"         = local.bucket_names_map["sot"]
    "--extra-py-files"        = local.glue_extra_py_files
  }

  # Juntando maps e criando dicionário único e definitivo de argumentos do job
  glue_job_default_arguments = merge(
    var.glue_job_general_arguments,
    local.glue_job_dynamic_arguments,
    var.glue_job_user_arguments
  )
}

# Chamando módulo glue
module "glue" {
  source = "./modules/glue"

  # Variáveis para ingestão do script do job no s3
  glue_app_dir         = var.glue_app_dir
  glue_app_src_dir     = var.glue_app_src_dir
  glue_job_bucket_name = module.storage.bucket_name_glue

  # Variáveis de configuração do job do glue
  glue_job_name                = var.glue_job_name
  glue_script_file_name        = var.glue_script_file_name
  glue_job_description         = var.glue_job_description
  glue_job_role_arn            = module.iam.iam_glue_role_arn
  glue_job_version             = var.glue_job_version
  glue_job_max_retries         = var.glue_job_max_retries
  glue_job_timeout             = var.glue_job_timeout
  glue_job_worker_type         = var.glue_job_worker_type
  glue_job_number_of_workers   = var.glue_job_number_of_workers
  glue_job_python_version      = var.glue_job_python_version
  glue_job_max_concurrent_runs = var.glue_job_max_concurrent_runs
  glue_job_default_arguments   = local.glue_job_default_arguments
}
