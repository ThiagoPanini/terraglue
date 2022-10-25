/* --------------------------------------------------
FILE: outputs.tf @ iam module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é permitir que outros
recursos definidos neste projeto possam utilizar 
policies e roles IAM aqui descritas.
-------------------------------------------------- */

output "iam_glue_role_arn" {
  value = aws_iam_role.glue_role.arn
}
