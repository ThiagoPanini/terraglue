/* ----------------------------------------------
FILE: main.tf @ root module

This is main Terraform file from the root module.
It contains all other modules calls with all
infrastructure needed to deploy the project.
The modules are:

- ./modules/storage
- ./modules/catalog
- ./modules/iam
- ./modules/glue

Details about each module can be found on each
one's main.tf file.
---------------------------------------------- */

# Defining data sources to help local variables
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
data "aws_kms_key" "s3" {
  key_id = var.s3_kms_key_alias
}


/* ----------------------------------------------
----------- TERRAFORM MODULE: storage -----------
  Creating storage resources on the AWS account
---------------------------------------------- */

# Defining local variables to be used on the module
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

# Calling the module
module "storage" {
  source = "./modules/storage"

  bucket_names_map            = local.bucket_names_map
  local_data_path             = var.local_data_path
  flag_upload_data_files      = var.flag_upload_data_files
  flag_s3_block_public_access = var.flag_s3_block_public_access
}


/* ----------------------------------------------
----------- TERRAFORM MODULE: catalog -----------
 Preparing the Data Catalog with local datasets
---------------------------------------------- */

# Defining local variables to be used on the module
locals {
  # Getting all files on the data path
  data_files = fileset(var.local_data_path, "**")

  # Getting database and tables names based on local folders
  db_names  = [for f in local.data_files : split("/", f)[0]]
  tbl_names = [for f in local.data_files : split("/", f)[1]]
  tbl_keys = [
    for i in range(length(local.db_names)) :
    "${local.db_names[i]}_${local.tbl_names[i]}"
  ]

  # Creating a list of each file's header
  file_headers = [
    for f in local.data_files : replace([
      for line in split("\n", file("${var.local_data_path}${f}")) :
      trimspace(line)
    ][0], "\"", "")
  ]

  # Crating a list for mapping column names
  column_names = [for c in local.file_headers : split(",", lower(c))]

  # Creating a list of s3 locations based on database and table names
  s3_locations = [
    for i in range(length(local.data_files)) :
    "s3://${module.storage.bucket_name_sor}/${local.db_names[i]}/${local.tbl_names[i]}"
  ]

  # Creating a final dictionary will all needed information
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

# Calling the module
module "catalog" {
  source = "./modules/catalog"

  # Variables for cataloging data
  glue_databases                      = local.db_names
  glue_catalog_map                    = local.glue_catalog_map
  catalog_table_parameters            = var.catalog_table_parameters
  catalog_table_input_format          = var.catalog_table_input_format
  catalog_table_output_format         = var.catalog_table_output_format
  catalog_table_serialization_library = var.catalog_table_serialization_library
  catalog_table_ser_de_parameters     = var.catalog_table_ser_de_parameters

  # Variables for athena configuration
  flag_create_athena_workgroup     = var.flag_create_athena_workgroup
  athena_workgroup_name            = var.athena_workgroup_name
  athena_workgroup_output_location = "s3://${module.storage.bucket_name_athena}"
  s3_kms_key_alias                 = var.s3_kms_key_alias

  depends_on = [
    module.storage
  ]
}

/* ----------------------------------------------
------------- TERRAFORM MODULE: iam -------------
 Setting up policies and a role for Glue service
---------------------------------------------- */

# Calling the module
module "iam" {
  source = "./modules/iam"

  iam_policies_path  = var.iam_policies_path
  iam_glue_role_name = var.iam_glue_role_name
}


/* ----------------------------------------------
------------- TERRAFORM MODULE: kms -------------
               Creating crypt keys
---------------------------------------------- */

# Defining local variables to be used on the module
locals {
  kms_policy_raw            = file("${var.kms_policy_path}/${var.kms_policy_file_name}")
  kms_policy_accountid_prep = replace(local.kms_policy_raw, "<account_id>", local.account_id)
  kms_policy_region_prep    = replace(local.kms_policy_accountid_prep, "<region>", local.region_name)
}

# Calling the module
module "kms" {
  source = "./modules/kms"

  kms_key_usage                = var.kms_key_usage
  kms_customer_master_key_spec = var.kms_customer_master_key_spec
  kms_is_enabled               = var.kms_is_enabled
  kms_enable_key_rotation      = var.kms_enable_key_rotation
  kms_policy                   = local.kms_policy_region_prep
}


/* ----------------------------------------------
------------ TERRAFORM MODULE: glue -------------
     Defining a Glue job with all parameters
---------------------------------------------- */


# Defining local variables to be used on the module
locals {
  # Getting extra Python files to be added on the job
  glue_extra_py_files = join(",", [
    for f in setsubtract(fileset(var.glue_app_src_dir, "**.py"), [var.glue_script_file_name]) :
    "s3://${module.storage.bucket_name_glue}/jobs/${var.glue_job_name}/src/${f}"
  ])

  # Defining variables to be used as job arguments
  output_bucket = local.bucket_names_map["sot"]
  output_table  = "tbsot_ecommerce_br"

  # Defining arguments for Glue job
  glue_job_arguments = {
    "--OUTPUT_BUCKET"                    = local.output_bucket
    "--OUTPUT_DB"                        = "db_ecommerce"
    "--OUTPUT_TABLE"                     = local.output_table
    "--OUTPUT_TABLE_URI"                 = "s3://${local.output_bucket}/${local.output_table}"
    "--CONNECTION_TYPE"                  = "s3"
    "--UPDATE_BEHAVIOR"                  = "UPDATE_IN_DATABASE"
    "--PARTITION_NAME"                   = "anomesdia"
    "--PARTITION_FORMAT"                 = "%Y%m%d"
    "--DATA_FORMAT"                      = "parquet"
    "--COMPRESSION"                      = "snappy"
    "--ENABLE_UPDATE_CATALOG"            = "True"
    "--NUM_PARTITIONS"                   = 5
    "--job-language"                     = "python"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--enable-metrics"                   = true
    "--enable-continuous-cloudwatch-log" = true
    "--enable-spark-ui"                  = true
    "--encryption-type"                  = "sse-s3"
    "--enable-glue-datacatalog"          = true
    "--enable-job-insights"              = true
    "--scriptLocation"                   = "s3://${local.bucket_names_map["glue"]}/scripts/"
    "--spark-event-logs-path"            = "s3://${local.bucket_names_map["glue"]}/sparkHistoryLogs/"
    "--TempDir"                          = "s3://${local.bucket_names_map["glue"]}/temporary/"
    "--extra-py-files"                   = local.glue_extra_py_files
    "--additional-python-modules"        = "sparksnake"
  }
}

# Calling the module
module "glue" {
  source = "./modules/glue"

  # Variables for uploading the script to S3
  glue_app_dir         = var.glue_app_dir
  glue_app_src_dir     = var.glue_app_src_dir
  glue_job_bucket_name = module.storage.bucket_name_glue

  # Variables for job details configuration
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
  glue_job_default_arguments   = local.glue_job_arguments
  glue_job_trigger_cron_expr   = var.glue_job_trigger_cron_expr

  # Variables for job security configuration
  glue_apply_security_configuration = var.glue_apply_security_configuration
  glue_cloudwatch_encryption_mode   = var.glue_cloudwatch_encryption_mode
  glue_job_bookmark_encryption_mode = var.glue_job_bookmark_encryption_mode
  glue_s3_encryption_mode           = var.glue_s3_encryption_mode
  glue_kms_key_arn                  = module.kms.kms_glue.arn
}
