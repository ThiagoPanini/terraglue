/* --------------------------------------------------
FILE: variables.tf @ root module

CONTEXT: Arquivo de especificação de variáveis a serem
utilizadas no módulo root desta especificação de infra

GOAL: O objetivo deste arquivo é centralizar a declaração
de variáveis importantes para o projeto, se tornando 
então uma foram de agilizar o desenvolvimento do código
através de um local organizado para uso das variáveis.
As variáveis alocadas neste arquivo são de uso 
exclusivo do arquivo main.tf no módulo root.
-------------------------------------------------- */

variable "aws_provider_config" {
  description = "Caminhos de configuração e credenciais do provedor AWS"
  type        = map(any)
  default = {
    "config"      = ["~/.aws/config"]
    "credentials" = ["~/.aws/credentials"]
  }
}

/* --------------------------------------------------
------------ VARIÁVEIS: módulo storage --------------
-------------------------------------------------- */

variable "local_data_path" {
  description = "Caminho local de armazenamento dos arquivos a serem inseridos no bucket s3"
  type        = string
  default     = "../data/"
}

variable "flag_upload_data_files" {
  description = "Flag para realização do upload de bases de dados"
  type        = bool
  default     = true
}

variable "flag_s3_block_public_access" {
  description = "Flag para configuração de bloqueio de acesso público de buckets criados"
  type        = bool
  default     = true
}

/* --------------------------------------------------
------------- VARIÁVEIS: módulo catalog -------------
-------------------------------------------------- */

variable "catalog_table_parameters" {
  description = "Parâmetros adicionais de criação da tabela (semelhante à cláusula TBLPROPERTIES do comando CREATE TABLE do Apache Hive)"
  type        = map(string)
  default = {
    "EXTERNAL"               = "TRUE"
    "skip.header.line.count" = "1"
  }
}

variable "catalog_table_input_format" {
  description = "Formato de entrada para armazenamento da tabela de acordo com classe Hive"
  type        = string
  default     = "org.apache.hadoop.mapred.TextInputFormat"
}

variable "catalog_table_output_format" {
  description = "Formato de saída para armazenamento da tabela de acordo com classe Hive"
  type        = string
  default     = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
}

variable "catalog_table_serialization_library" {
  description = "Biblioteca principal de serialização para criação e especificação dos metadados da tabela no catálogo"
  type        = string
  default     = "org.apache.hadoop.hive.serde2.OpenCSVSerde"
}

variable "catalog_table_ser_de_parameters" {
  description = "Parâmetros de serialização e deserialização com base na biblioteca de serialização definida"
  type        = map(string)
  default = {
    "separatorChar" = ","
    "quoteChar"     = "\"",
    "escapeChar"    = "\\"
  }
}

variable "flag_create_athena_workgroup" {
  description = "Flag para guiar a criação opção de um workgroup pré configurado para o Amazon Athena"
  type        = bool
  default     = true
}

variable "athena_workgroup_name" {
  description = "Nome do workgoup a ser criado para o Athena (apenas caso var.flag_create_athena_workgroup=true)"
  type        = string
  default     = "sbx-analytics-workgroup"
}

variable "s3_kms_key_alias" {
  description = "Alias de chave KMS a ser utilizada na criptografia dos resultados de query no bucket do Athena"
  type        = string
  default     = "alias/aws/s3"
}


/* --------------------------------------------------
--------------- VARIÁVEIS: módulo iam ---------------
-------------------------------------------------- */

variable "iam_policies_path" {
  description = "Caminho no sistema onde as políticas do IAM estão armazenadas em formato JSON"
  type        = string
  default     = "./modules/iam/policy"
}

variable "iam_glue_role_name" {
  description = "Nome da role criada para execução de jobs do Glue"
  type        = string
  default     = "terraglue-glue-execution-role"
}


/* --------------------------------------------------
-------------- VARIÁVEIS: módulo glue ---------------
-------------------------------------------------- */

variable "glue_job_script_file" {
  description = "Localização física do script .py a ser implantado como um job do glue"
  type        = string
  default     = "../app/src/main-terraglue.py"
}


variable "glue_job_bucket_scripts_key" {
  description = "Chave de armazenamento do script do job do glue no bucket s3 de referência"
  type        = string
  default     = "scripts/"
}

variable "glue_job_name" {
  description = "Nome ou referência do job do glue a ser criado"
  type        = string
  default     = "gluejob-sot-ecommerce-br"
}

variable "glue_job_description" {
  description = "Descrição do job do glue criado no projeto"
  type        = string
  default     = "Job criado para construção de tabela na camada SoT contendo dados preparados de vendas online do e-commerce brasileiro"
}

variable "glue_job_version" {
  description = "Versão do glue a ser utilizada na execução do job"
  type        = string
  default     = "3.0"
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

variable "glue_job_worker_type" {
  description = "Tipo do nó worker responsável por processar os dados no job"
  type        = string
  default     = "G.1X"
}

variable "glue_job_number_of_workers" {
  description = "Número de workers utilizados para processamento e execução do job"
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

variable "glue_job_general_arguments" {
  description = "Conjunto de argumentos padrão a serem associados ao job do glue"
  type        = map(string)
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

variable "glue_job_user_arguments" {
  description = "Conjunto de argumentos personalizados do usuário a serem associados ao job do glue"
  type        = map(string)
  default = {
    "--OUTPUT_DB"             = "ra8"
    "--OUTPUT_TABLE"          = "tbsot_ecommerce_br"
    "--CONNECTION_TYPE"       = "s3"
    "--UPDATE_BEHAVIOR"       = "UPDATE_IN_DATABASE"
    "--PARTITION_NAME"        = "anomesdia"
    "--PARTITION_FORMAT"      = "%Y%m%d"
    "--DATA_FORMAT"           = "parquet"
    "--COMPRESSION"           = "snappy"
    "--ENABLE_UPDATE_CATALOG" = "True"
  }
}
