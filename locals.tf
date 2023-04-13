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



  /*
  # Checks if users want to create a KMS key and assign the ARN of the KMS key resource created if so
  iam_role_arn = var.flag_create_iam_role ? aws_kms_key.glue_cmk[0].arn : var.kms_key_arn

  # Checks if users want to create a KMS key and assign the ARN of the KMS key resource created if so
  kms_key_arn = var.flag_create_kms_key ? aws_kms_key.glue_cmk[0].arn : var.kms_key_arn

  # Referencing a policies folder where the JSON files for policies are located
  iam_policies_path = "${path.module}/policy/"

  # Getting all files to be uploaded do S3 as useful elements for the Glue job
  glue_files = fileset(path.module, "${var.glue_app_dir}{${join(",", var.subfolders_to_upload)}}/*{${join(",", var.file_extensions_to_upload)}}")
  */

  /* --------------------------------------------------------
  ------------------ VALIDATING VARIABLES -------------------
  -----------------------------------------------------------

  According to discussions in the issue #25609 of the source
  Terraform project (the official one), Terraform can't handle
  variables validation using a condition that references other
  variable but the one which is been validated.

  It means that if users want to apply a validate condition
  in a Terraform variable (e.g. "x") that uses information about
  another Terraform variable (e.g. "y"), the error below is
  thrown:

  The condition for variable "x" can only refer to the variable
  itself, using var.y.

  So, according to
  https://github.com/hashicorp/terraform/issues/25609,
  @gdsotirov provided a temporary solution that uses the
  output clause with its new precondition block (since 
  Terraform v1.2.0) to apply custom condition checks in
  Terraform variables.

  Workaround using locals:
  https://github.com/hashicorp/terraform/issues/25609#issuecomment-1057614400
  -------------------------------------------------------- */
  validate_glue_role_arn = (var.mode != "learning" && var.flag_create_iam_role == false && var.glue_role_arn == "") ? tobool("The module was configured to not create an IAM role (var.flag_create_iam_role = false) but it wasn't passed any IAM role ARN to be assumed by the Glue job.") : true
  validate_kms_key_arn   = (var.mode != "learning" && var.flag_create_kms_key == false && var.kms_key_arn == "") ? tobool("The module was configured to not create a KMS key (var.flag_create_kms_key = false) but it wasn't passed any KMS key ARN to be used in Glue job encryption tasks.") : true
}
