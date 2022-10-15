/* --------------------------------------------------
FILE: outputs.tf @ iam module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é permitir que outros
recursos definidos neste projeto possam utilizar 
policies e roles IAM aqui descritas.
-------------------------------------------------- */

variable "iam_policies_path" {
  description = "Caminho no sistema onde as políticas do IAM estão armazenadas em formato JSON"
  type        = string
}
