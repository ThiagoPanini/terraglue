/* --------------------------------------------------
FILE: variables.tf @ analytics module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis para toda a construção do ambiente de
utilização do Glue na AWS
-------------------------------------------------- */

variable "local_data_path" {
  description = "Caminho local de armazenamento dos arquivos a serem inseridos no bucket s3"
  type        = string
}

variable "glue_databases" {
  description = "Referências dos databases a serem criados no catálogo de dados do Glue para recebimento das tabelas"
  type        = list(string)
}
