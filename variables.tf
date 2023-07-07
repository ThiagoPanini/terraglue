/* --------------------------------------------------------
FILE: variables.tf @ root module

This file contains all variables used on this IaC project.
As much as the project is divided in different modules,
this variables.tf file from root module is where users
can set all variables used on all other modules.

This variable file can be summarized by the following topics:

1. IAM variables
2. KMS variables
3. Glue variables
  3.1 Glue variables to upload files to S3
  3.2 Glue variables to set the security configuration
  3.3 Glue variables to configure the job
  3.4 Glue variables to handle required info on learning mode
-------------------------------------------------------- */

variable "mode" {
  description = "Defines an operation mode that enables users to choose to use the module for learning or production/development purposes"
  type        = string
  default     = "production"

  validation {
    condition     = contains(["learning", "production"], var.mode)
    error_message = "Acceptable values for mode variable are: 'learning', 'production'"
  }
}


/* --------------------------------------------------------
--------------------- VARIABLES: iam ----------------------
-------------------------------------------------------- */

variable "flag_create_iam_role" {
  description = "Flag that enables the creation of an IAM role within the module"
  type        = bool
  default     = false
}

variable "glue_policies_path" {
  description = "Folder where JSON files are located in order to create IAM policies for a Glue IAM role. Users should pass this variable in case of var.flag_create_iam_role is true"
  type        = string
  default     = "policy/glue"
}

variable "glue_role_name" {
  description = "Role name for IAM role to be assumed by a Glue job. This variable is used just in case of var.flag_create_iam_role is true or when var.mode = learning"
  type        = string
  default     = "terraglue-glue-job-role"
}

variable "glue_role_arn" {
  description = "IAM role ARN to be assumed by the Glue job. Users must pass this variable in case of var.flag_create_iam_role is false"
  type        = string
  default     = ""
}


/* --------------------------------------------------------
--------------------- VARIABLES: kms ----------------------
-------------------------------------------------------- */

variable "flag_create_kms_key" {
  description = "Flag that enables the creation of a KMS key to be used in the Glue job security configuration"
  type        = bool
  default     = false
}

variable "kms_policies_path" {
  description = "Folder where JSON files are located in order to create IAM policies for a KMS key. Users should pass this variable in case of var.flag_create_kms_key is true"
  type        = string
  default     = "policy/kms"
}

variable "kms_key_alias" {
  description = "Alias for the KMS key created. Users should pass this variable in case of var.flag_create_kms_key is true"
  type        = string
  default     = "alias/kms-glue-s3"

  validation {
    condition     = substr(var.kms_key_alias, 0, 6) == "alias/"
    error_message = "Variable kms_key_alias must start with 'alias/' prefix. Example: alias/kms-glue-s3"
  }
}

variable "kms_key_arn" {
  description = "KMS key ARN to encrypt data generated by the Glue job. Users must pass this variable in case of var.flag_create_kms_key is false"
  type        = string
  default     = ""
}


/* --------------------------------------------------------
--------------------- VARIABLES: glue ---------------------
              Usage: Upload Glue files to S3
-------------------------------------------------------- */

variable "glue_app_dir" {
  description = "Application directory where Glue subfolders and files that should be uploaded do S3 are located. It references the root Terraform module where terraglue is called from"
  type        = string
  default     = "app"

  validation {
    condition     = can(regex("^[0-9A-Za-z]+$", var.glue_app_dir))
    error_message = "The application dir value has special characteres. Only a-z, A-Z and 0-9 characteres are allowed."
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

variable "glue_scripts_bucket_name" {
  description = "Bucket name where Glue application files will be stored"
  type        = string
}

variable "glue_scripts_bucket_prefix" {
  description = "An optional S3 prefix to organize Glue application files"
  type        = string
  default     = "jobs/"

  validation {
    condition     = var.glue_scripts_bucket_prefix == "" || substr(var.glue_scripts_bucket_prefix, -1, -1) == "/"
    error_message = "The prefix to store the glue scripts must not be empty and it must end with '/'."
  }
}

variable "glue_main_script_path" {
  description = "Location of the python file to be assumed as the main Spark application script for the Glue job. The path reference is the root Terraform module where terraglue is called"
  type        = string
  default     = "app/src/main.py"
}


/* --------------------------------------------------------
--------------------- VARIABLES: glue ---------------------
              Usage: Security Configuration
-------------------------------------------------------- */

variable "glue_apply_security_configuration" {
  description = "Flag to guide the application of the Security Configuration to the Glue job"
  type        = bool
  default     = true
}

variable "glue_cloudwatch_encryption_mode" {
  description = "Encryption definition for CloudWatch logs generated on the Glue job in order to set the job security configuration"
  type        = string
  default     = "SSE-KMS"
}

variable "glue_job_bookmark_encryption_mode" {
  description = "Encryption definition for job bookmarks on Glue job in order to set the job security configuration"
  type        = string
  default     = "DISABLED"
}

variable "glue_s3_encryption_mode" {
  description = "Encryption definition for s3 data generated on the Glue job in order to set the job security configuration"
  type        = string
  default     = "SSE-KMS"
}


/* --------------------------------------------------------
--------------------- VARIABLES: glue ---------------------
                Usage: Job configuration
-------------------------------------------------------- */

variable "glue_job_name" {
  description = "A name reference for the Glue job to be created"
  type        = string
  default     = "terraglue-sample-job"
}

variable "glue_job_description" {
  description = "A short description for the Glue job"
  type        = string
  default     = "An example of a Glue job from the terraglue source Terraform module"
}

variable "glue_job_version" {
  description = "Glue version for the job to be created"
  type        = string
  default     = "4.0"
}

variable "glue_job_max_retries" {
  description = "Max retries in cases of running the job with failures"
  type        = string
  default     = "0"
}

variable "glue_job_timeout" {
  description = "Timeout (in minutes) for job execution"
  type        = number
  default     = 10
}

variable "glue_job_worker_type" {
  description = "Node/worker type to process data in AWS managed Glue cluster"
  type        = string
  default     = "G.1X"
}

variable "glue_job_number_of_workers" {
  description = "Number of workers to process data in AWS managed Glue cluster"
  type        = number
  default     = 3
}

variable "glue_job_python_version" {
  description = "Python version to be used in the job"
  type        = string
  default     = "3"
}

variable "glue_job_max_concurrent_runs" {
  description = "Max number of concurrent runs for the job"
  type        = number
  default     = 2
}

variable "glue_job_args" {
  description = "A map of all job arguments to be deployed within the Glue job"
  type        = map(any)
  default = {
    "--job-language"                     = "python"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--enable-metrics"                   = true
    "--enable-continuous-cloudwatch-log" = true
    "--enable-spark-ui"                  = true
    "--encryption-type"                  = "sse-s3"
    "--enable-glue-datacatalog"          = true
    "--enable-job-insights"              = true
  }
}


/* --------------------------------------------------------
--------------------- VARIABLES: glue ---------------------
   Usage: Required information when using learning mode
-------------------------------------------------------- */

variable "job_output_bucket_name" {
  description = "The name of the S3 output bucket for the Glue job when calling the module on learning mode"
  type        = string
  default     = ""
}

variable "job_output_database" {
  description = "The name of the Glue database for the Glue job when calling the module on learning mode"
  type        = string
  default     = ""
}

