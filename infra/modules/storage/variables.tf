/* --------------------------------------------------
FILE: variables.tf @ storage module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis para toda a construção do ambiente de
armazenamento dos dados e insumos no s3
-------------------------------------------------- */

variable "bucket_names_map" {
  description = "Map contendo chaves e nomes de todos os buckets a serem criados no projeto"
  type        = map(string)
}

variable "local_data_path" {
  description = "Caminho local de armazenamento dos arquivos a serem inseridos no bucket s3"
  type        = string
}

variable "flag_upload_data_files" {
  description = "Flag para realização do upload de bases de dados"
  type        = bool
}

variable "flag_s3_block_public_access" {
  description = "Flag para configuração de bloqueio de acesso público de buckets criados"
  type        = bool
}
