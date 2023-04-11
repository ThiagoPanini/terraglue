/* --------------------------------------------------------
FILE: variables.tf @ root module

This file contains all variables used on this IaC project.
As much as the project is divided in different modules,
this variables.tf file from root module is where users
can set all variables used on all other modules.
-------------------------------------------------------- */

variable "aws_provider_config" {
  description = "Providing a local file where AWS credentials are stored"
  type        = map(any)
  default = {
    "config"      = ["~/.aws/config"]
    "credentials" = ["~/.aws/credentials"]
  }
}


/* --------------------------------------------------------
--------------------- VARIABLES: iam ----------------------
-------------------------------------------------------- */

variable "glue_role_name" {
  description = "Role name for IAM role to be assumed by a Glue job"
  type        = string
  default     = "terraglue-glue-job-role"
}


/* --------------------------------------------------------
--------------------- VARIABLES: kms ----------------------
-------------------------------------------------------- */

variable "flag_create_kms_key" {
  description = "Flag that enables or disables the creation of a KMS Key to be used in the Glue job security configuration"
  type        = bool
  default     = true
}


/* --------------------------------------------------------
--------------------- VARIABLES: glue ---------------------
-------------------------------------------------------- */
