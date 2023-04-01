/* ----------------------------------------------
FILE: variables.tf @ root module

This file contains all variables used on this IaC
project. 

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
------------ VARIÁVEIS: módulo kms --------------
-------------------------------------------------- */
variable "kms_key_usage" {
  description = "Específica a intenção de uso da chave"
  type        = string
  default     = "ENCRYPT_DECRYPT"
}

variable "kms_customer_master_key_spec" {
  description = "Específica se a chave KMS contém uma chave simétrica ou assimétrica"
  type        = string
  default     = "SYMMETRIC_DEFAULT"
}

variable "kms_is_enabled" {
  description = "Flag para indicar se a chave está habilitada"
  type        = bool
  default     = true
}

variable "kms_enable_key_rotation" {
  description = "Flag para habilitar a rotação da chave"
  type        = bool
  default     = false
}

variable "kms_policy_path" {
  description = "Caminho local onde o arquivo JSON contendo a policy da chave KMS está localizado"
  type        = string
  default     = "./modules/kms/policy"
}

variable "kms_policy_file_name" {
  description = "Nome do arquivo JSON contendo a policy da chave KMS"
  type        = string
  default     = "kms-key-policy.json"
}


/* --------------------------------------------------
-------------- VARIÁVEIS: módulo glue ---------------
-------------------------------------------------- */

variable "glue_app_dir" {
  description = "Referência local do diretório onde a aplicação está localizada"
  type        = string
  default     = "../app"
}

variable "glue_app_src_dir" {
  description = "Referência de diretório onde os códigos fontes da aplicação estão localizados"
  type        = string
  default     = "../app/src"
}

variable "glue_app_utils_dir" {
  description = "Referência local do diretório onde os módulos Python auxiliares estão armazenados"
  type        = string
  default     = "../app/src/utils"
}

variable "glue_extra_py_files" {
  description = "Listagem com todos os caminhos, com ponto de referência em relação ao diretório /app/src, de todos os módulos .py adicionais a serem utilizados no job do Glue"
  type        = list(string)
  default     = ["terraglue.py"]
}

variable "glue_script_file_name" {
  description = "Referência do script .py a ser implantado como um job do glue"
  type        = string
  default     = "main.py"
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
  default     = 3
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
    "--OUTPUT_DB"             = "db_ecommerce"
    "--OUTPUT_TABLE"          = "tbsot_ecommerce_br"
    "--CONNECTION_TYPE"       = "s3"
    "--UPDATE_BEHAVIOR"       = "UPDATE_IN_DATABASE"
    "--PARTITION_NAME"        = "anomesdia"
    "--PARTITION_FORMAT"      = "%Y%m%d"
    "--DATA_FORMAT"           = "parquet"
    "--COMPRESSION"           = "snappy"
    "--ENABLE_UPDATE_CATALOG" = "True"
    "--NUM_PARTITIONS"        = 5
  }
}

variable "glue_job_trigger_cron_expr" {
  description = "Expressão cron responsável pelo agendamento do job do Glue"
  type        = string
  default     = "cron(0 21 ? * 6 *)"
}

variable "glue_apply_security_configuration" {
  description = "Flag para definição da aplicação da configuração de segurança ao job do Glue"
  type        = bool
  default     = true
}

variable "glue_cloudwatch_encryption_mode" {
  description = "Definição de criptografia para logs do CloudWatch gerados no job do Glue para configuração de segurança"
  type        = string
  default     = "SSE-KMS"
}

variable "glue_job_bookmark_encryption_mode" {
  description = "Definição de criptografia para job bookmarks no job do Glue para configuração de segurança"
  type        = string
  default     = "DISABLED"
}

variable "glue_s3_encryption_mode" {
  description = "Definição de criptografia para dados escritos no s3 gerados no job do Glue para configuração de segurança"
  type        = string
  default     = "SSE-KMS"
}
