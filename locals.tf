/* --------------------------------------------------------
FILE: locals.tf

This file handles declaration of locals variables that can
be used along other Terraform files to help users to
organize elements and componentes for all resources to be
deployed in this infrastructure project
-------------------------------------------------------- */

# Defining data sources to help local variables
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Defining local values to be used on the module
locals {
  # If in learning mode, considers the path.module value to reference the JSON policy for Glue job. Else, considers the user input
  glue_policies_path = var.mode == "learning" ? "${path.module}/policy/glue/" : var.glue_policies_path

  # If in learning mode, considers the path.module value to reference the JSON policy for KMS key. Else, considers the user input
  kms_policies_path = var.mode == "learning" ? "${path.module}/policy/kms/" : var.kms_policies_path

  # Assigning the IAM role and KMS key ARN according to module variables
  glue_role_arn = var.mode == "learning" || var.flag_create_iam_role ? aws_iam_role.glue_job_role[0].arn : var.glue_role_arn
  kms_key_arn   = var.mode == "learning" || var.flag_create_kms_key ? aws_kms_key.glue_cmk[0].arn : var.kms_key_arn

  # Defining a pattern to fileset Terraform function in order to collect all application subfolders and files to upload to S3
  fileset_pattern = "${var.glue_app_dir}/{${join(",", var.subfolders_to_upload)}}/*{${join(",", var.file_extensions_to_upload)}}"

  # Getting all Glue files to be uploaded to S3 according to module mode
  glue_files_learning_mode   = fileset(path.module, local.fileset_pattern)
  glue_files_production_mode = fileset(path.root, local.fileset_pattern)

  # Getting all files to be uploaded do S3 as useful elements for the Glue job
  glue_files = var.mode == "learning" ? local.glue_files_learning_mode : local.glue_files_production_mode

  # Assigning the local source of glue files according to module mode
  glue_files_root_source = var.mode == "learning" ? path.module : path.root

  # Defining the key of each glue file to be stored in S3
  glue_files_key = "${var.glue_scripts_bucket_prefix}${var.glue_job_name}"

  # Creating a local value for the script location in S3
  glue_script_location = "s3://${var.glue_scripts_bucket_name}/${var.glue_scripts_bucket_prefix}${var.glue_job_name}/${var.glue_main_script_path}"

  # Extracting the job main script name
  glue_script_file_name = split("/", var.glue_main_script_path)[0]

  # Creating a reference for extra python files to be included in the job
  glue_extra_py_files = join(",", [
    for f in setsubtract(local.glue_files, [var.glue_main_script_path]) :
    "s3://${var.glue_scripts_bucket_name}/${var.glue_scripts_bucket_prefix}${var.glue_job_name}/${f}"
    if length(regexall(".py", f)) > 0
  ])

  # Creating a map of custom arguments to be used in case of calling the mode with learning mode
  glue_job_custom_args = {
    "--OUTPUT_BUCKET"                    = var.job_output_bucket_name
    "--OUTPUT_DB"                        = var.job_output_database
    "--OUTPUT_TABLE"                     = "tbsot_ecommerce_data"
    "--OUTPUT_TABLE_URI"                 = "s3://${var.job_output_bucket_name}/tbsot_ecommerce_data"
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
    "--spark-event-logs-path"            = "s3://${var.glue_scripts_bucket_name}/sparkHistoryLogs/"
    "--TempDir"                          = "s3://${var.glue_scripts_bucket_name}/temporary/"
    "--extra-py-files"                   = local.glue_extra_py_files
    "--additional-python-modules"        = "sparksnake"
  }

  # Adding job arguments if module is called with learning mode
  glue_job_args = var.mode == "learning" ? merge(var.glue_job_args, local.glue_job_custom_args) : var.glue_job_args

  /* --------------------------------------------------------
  ------------------ VALIDATING VARIABLES -------------------
  -----------------------------------------------------------

  According to discussions in the issue #25609 of the source
  Terraform project (the official one), Terraform can't handle
  variables validation using a condition that references multiple
  variables.

  It means that if users want to apply a validate condition
  in a variable (e.g. "x") using information about another 
  variable (e.g. "y"), the error below is thrown:

  The condition for variable "x" can only refer to the variable
  itself, using var.y.

  Workarounds:
  https://github.com/hashicorp/terraform/issues/25609,
  https://github.com/hashicorp/terraform/issues/25609#issuecomment-1057614400
  -------------------------------------------------------- */

  # Validating ARNs for IAM role and KMS key
  validate_glue_role_arn = (var.mode != "learning" && var.flag_create_iam_role == false && var.glue_role_arn == "") ? tobool("The module was configured to not create an IAM role (var.flag_create_iam_role = false) but it wasn't passed any IAM role ARN to be assumed by the Glue job.") : true
  validate_kms_key_arn   = (var.mode != "learning" && var.flag_create_kms_key == false && var.kms_key_arn == "") ? tobool("The module was configured to not create a KMS key (var.flag_create_kms_key = false) but it wasn't passed any KMS key ARN to be used in Glue job encryption tasks.") : true

  # Validating output bucket and database variables when learning mode is called
  validate_output_bucket_name = (var.mode == "learning" && var.job_output_bucket_name == "") ? tobool("When calling the module with learning mode, it's necessary to provide a valid bucket name for the job_output_bucket_name variable") : true
  validate_output_database    = (var.mode == "learning" && var.job_output_database == "") ? tobool("When calling the module with learning mode, it's necessary to provide a database name for the job_output_db variable") : true
}
