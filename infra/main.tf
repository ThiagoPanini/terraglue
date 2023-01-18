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
data "aws_kms_key" "s3" {
  key_id = var.s3_kms_key_alias
}


/* --------------------------------------------------
------------- MÓDULO TERRAFORM: storage -------------
      Criando recursos de armazenamento na conta
-------------------------------------------------- */

# Definindo variáveis locais para uso no módulo
locals {
  account_id  = data.aws_caller_identity.current.account_id
  region_name = data.aws_region.current.name

  bucket_names_map = {
    "sor"    = "terraglue-sor-data-${local.account_id}-${local.region_name}"
    "sot"    = "terraglue-sot-data-${local.account_id}-${local.region_name}"
    "spec"   = "terraglue-spec-data-${local.account_id}-${local.region_name}"
    "athena" = "terraglue-athena-query-results-${local.account_id}-${local.region_name}"
    "glue"   = "terraglue-glue-assets-${local.account_id}-${local.region_name}"
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
  source = "./modules/iam"

  # Variáveis para criação das policies e roles
  iam_policies_path  = var.iam_policies_path
  iam_glue_role_name = var.iam_glue_role_name
}


/* --------------------------------------------------
-------------- MÓDULO TERRAFORM: kms ---------------
      Criação de chave KMS para criptografia
-------------------------------------------------- */

# Variáveis locais para um melhor gerenciamento dos recursos do módulo
locals {
  kms_policy_raw  = file("${var.kms_policy_path}/${var.kms_policy_file_name}")
  kms_policy_prep = replace(local.kms_policy_raw, "<account_id>", local.account_id)
}

# Chamando módulo kms
module "kms" {
  source = "./modules/kms"

  # Variáveis para configuração da chave
  kms_key_usage                = var.kms_key_usage
  kms_customer_master_key_spec = var.kms_customer_master_key_spec
  kms_is_enabled               = var.kms_is_enabled
  kms_enable_key_rotation      = var.kms_enable_key_rotation
  kms_policy                   = local.kms_policy_prep
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
  glue_job_trigger_cron_expr   = var.glue_job_trigger_cron_expr

  # Variáveis de configuração de segurança do job
  glue_apply_security_configuration = var.glue_apply_security_configuration
  glue_cloudwatch_encryption_mode   = var.glue_cloudwatch_encryption_mode
  glue_job_bookmark_encryption_mode = var.glue_job_bookmark_encryption_mode
  glue_s3_encryption_mode           = var.glue_s3_encryption_mode
  glue_kms_key_arn                  = module.kms.kms_glue.arn
}
