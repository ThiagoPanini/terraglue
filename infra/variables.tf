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

variable "iam_policies_path" {
  description = "Caminho no sistema onde as políticas do IAM estão armazenadas em formato JSON"
  type        = string
  default     = "./modules/iam/policy"
}
