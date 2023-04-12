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
  # Referencing a policies folder where the JSON files for policies are located
  iam_policies_path = "${path.module}/policy/"

  # Getting all files to be uploaded do S3 as useful elements for the Glue job
  glue_files = fileset(path.module, "${var.glue_app_dir}{${join(",", var.subfolders_to_upload)}}/*{${join(",", var.file_extensions_to_upload)}}")

  # Tests if users want to create a KMS key
  kms_key_arn = var.flag_create_kms_key ? aws_kms_key.glue_cmk[0].arn : var.kms_key_arn
}

output "kms_key_arn" {
  value = local.kms_key_arn
}
