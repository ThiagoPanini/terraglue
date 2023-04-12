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

variable "glue_app_dir" {
  description = "Reference for the application directory where all the needed files to run the Glue job are stored"
  type        = string
  default     = "app/"

  validation {
    condition     = can(regex("^[0-9A-Za-z]+/$", var.glue_app_dir))
    error_message = "The application dir value must end with '/' and only a-z, A-Z and 0-9 are allowed."
  }
}

variable "subfolders_to_upload" {
  description = "A list with all valid subfolders located in the var.glue_app_dir variable that will be uploaded to S3"
  type        = list(string)
  default     = ["src", "sql", "utils"]
}

variable "file_extensions_to_upload" {
  description = "A list with all valid file extensions for files in glue_scripts_local_dir variable to be uploaded to S3"
  type        = list(string)
  default     = [".py", ".json", ".sql"]
}

variable "glue_scripts_s3_bucket" {
  description = "Bucket name where Glue application files will be stored"
  type        = string
  # ToDo: Remove default to force users to pass it
  default = "datadelivery-glue-assets-905781841335-us-east-1"
}

variable "glue_scripts_s3_bucket_prefix" {
  description = "An optional S3 prefix to organize Glue application files"
  type        = string
  # ToDo: Remove default to force users to pass it
  default = "gluejobsotecommerce"
}
