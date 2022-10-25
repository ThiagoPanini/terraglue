/* --------------------------------------------------
FILE: variables.tf @ iam module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis para a criação de políticas e roles iam
responsáveis por permitir acessos aos recursos 
utilizados neste projeto
-------------------------------------------------- */

variable "iam_policies_path" {
  description = "Caminho no sistema onde as políticas do IAM estão armazenadas em formato JSON"
  type        = string
}

variable "iam_glue_role_name" {
  description = "Nome da role criada para execução de jobs do Glue"
  type = string
}
