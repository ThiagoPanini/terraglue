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

variable "glue_job_bucket_name" {
  description = "Bucket name used to upload the job application script"
  type        = string
}

variable "glue_job_name" {
  description = "Glue job name"
  type        = string
  default     = "terraglue-gluejob-example"
}

variable "glue_script_file_name" {
  description = "Name of the main script used as the job application"
  type        = string
  default     = "main.py"
}

variable "glue_job_description" {
  description = "A short description for the job"
  type        = string
  default     = ""
}

variable "glue_job_role_arn" {
  description = "ARN of the IAM role to be assumed by the Glue job"
  type        = string
}

variable "glue_job_version" {
  description = "Glue job version"
  type        = string
  default     = "4.0"
}

variable "glue_job_worker_type" {
  description = "Glue job worker type"
  type        = string
  default     = "G.1X"
}

variable "glue_job_number_of_workers" {
  description = "Número de workers utilizados para processamento e execução do job"
  type        = number
  default     = 3
}

variable "glue_job_max_retries" {
  description = "Tentativas máximas de execução do job em caso de falhas"
  type        = string
  default     = "0"
}

variable "glue_job_timeout" {
  description = "Tempo máximo (em minutos) de execução do job até retornar um erro de timeout"
  type        = number
  default     = 10
}

variable "glue_job_python_version" {
  description = "Versão do Python a ser utilizada na implantação do job"
  type        = string
  default     = "3"
}

variable "glue_job_max_concurrent_runs" {
  description = "Número máximo de execuções concorrrentes permitida para o job"
  type        = number
  default     = 2
}

variable "glue_job_default_arguments" {
  description = "Dicionário contendo mapeamentos para todos os argumentos e seus respectivos valores configurados para o job do glue"
  type        = map(string)
}

variable "glue_job_trigger_cron_expr" {
  description = "Expressão cron responsável pelo agendamento do job do Glue na AWS"
  type        = string
  default     = "cron(0 21 ? * 6 *)"
}

variable "glue_apply_security_configuration" {
  description = "Flag para definição da aplicação da configuração de segurança ao job do Glue"
  type        = bool
}

variable "glue_cloudwatch_encryption_mode" {
  description = "Definição de criptografia para logs do CloudWatch gerados no job do Glue para configuração de segurança"
  type        = string
}

variable "glue_job_bookmark_encryption_mode" {
  description = "Definição de criptografia para job bookmarks no job do Glue para configuração de segurança"
  type        = string
}

variable "glue_s3_encryption_mode" {
  description = "Definição de criptografia para dados escritos no s3 gerados no job do Glue para configuração de segurança"
  type        = string
}

variable "glue_kms_key_arn" {
  description = "ARN da chave KMS utilizada para criptografia dos insumos na configuração de segurança do job"
  type        = string
}
