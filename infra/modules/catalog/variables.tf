/* --------------------------------------------------
FILE: variables.tf @ catalog module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis para toda a construção do ambiente de
utilização do Glue na AWS
-------------------------------------------------- */

variable "glue_databases" {
  description = "Referências dos databases a serem criados no catálogo de dados do Glue para recebimento das tabelas"
  type        = list(string)
}

variable "glue_catalog_map" {
  description = "Dicionário contendo todas as informações necessárias para inserção de entradas (tabelas) no catálogo de dados do Glue"
  type        = map(any)
}

variable "catalog_table_parameters" {
  description = "Parâmetros adicionais de criação da tabela (semelhante à cláusula TBLPROPERTIES do comando CREATE TABLE do Apache Hive)"
  type        = map(string)
}

variable "catalog_table_input_format" {
  description = "Formato de entrada para armazenamento da tabela de acordo com classe Hive"
  type        = string
}

variable "catalog_table_output_format" {
  description = "Formato de saída para armazenamento da tabela de acordo com classe Hive"
  type        = string
}

variable "catalog_table_serialization_library" {
  description = "Biblioteca principal de serialização para criação e especificação dos metadados da tabela no catálogo"
  type        = string
}

variable "catalog_table_ser_de_parameters" {
  description = "Parâmetros de serialização e deserialização com base na biblioteca de serialização definida"
  type        = map(string)
}

variable "flag_create_athena_workgroup" {
  description = "Flag para guiar a criação opção de um workgroup pré configurado para o Amazon Athena"
  type        = bool
}

variable "athena_workgroup_name" {
  description = "Nome do workgoup a ser criado para o Athena (apenas caso var.flag_create_athena_workgroup=true)"
  type        = string
}

variable "athena_workgroup_output_location" {
  description = "URL de bucket utilizado para armazenamento dos resultados de query no AThena (apenas caso var.flag_create_athena_workgroup=true)"
  type        = string
}

variable "s3_kms_key_alias" {
  description = "Alias de chave KMS a ser utilizada na criptografia dos resultados de query no bucket do Athena"
  type        = string
}
