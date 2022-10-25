/* --------------------------------------------------
FILE: variables.tf @ glue module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis para a criação de um job do Glue
-------------------------------------------------- */

variable "glue_job_bucket_name" {
  description = "Nome do bucket a ser utilizado para upload do script do job"
  type        = string
}

variable "glue_job_bucket_scripts_key" {
  description = "Chave de armazenamento do script do job do glue no bucket s3 de referência"
  type        = string
}

variable "glue_job_name" {
  description = "Nome ou referência do job do glue a ser criado"
  type        = string
}

variable "glue_job_script_file" {
  description = "Referência local do script a ser utilizado como job do glue"
  type        = string
}

variable "glue_job_description" {
  description = "Descrição do job do glue criado no projeto"
  type        = string
}

variable "glue_job_role_arn" {
  description = "ARN da role de execução do job do Glue"
  type        = string
}

variable "glue_job_version" {
  description = "Versão do glue a ser utilizada na execução do job"
  type        = string
}

variable "glue_job_worker_type" {
  description = "Tipo do nó worker responsável por processar os dados no job"
  type        = string
}

variable "glue_job_number_of_workers" {
  description = "Número de workers utilizados para processamento e execução do job"
  type        = number
}

variable "glue_job_max_retries" {
  description = "Tentativas máximas de execução do job em caso de falhas"
  type        = string
}

variable "glue_job_timeout" {
  description = "Tempo máximo (em minutos) de execução do job até retornar um erro de timeout"
  type        = number
}

variable "glue_job_python_version" {
  description = "Versão do Python a ser utilizada na implantação do job"
  type        = string
}

variable "glue_job_max_concurrent_runs" {
  description = "Número máximo de execuções concorrrentes permitida para o job"
  type        = number
}

variable "glue_job_default_arguments" {
  description = "Dicionário contendo mapeamentos para todos os argumentos e seus respectivos valores configurados para o job do glue"
  type        = map(string)
}
