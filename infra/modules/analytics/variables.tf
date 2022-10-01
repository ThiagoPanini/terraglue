/* --------------------------------------------------
FILE: variables.tf @ analytics module

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
