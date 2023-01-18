/* --------------------------------------------------
FILE: outputs.tf @ kms module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é permitir que outros
recursos definidos neste projeto possam utilizar 
a chave KMS criada
-------------------------------------------------- */

output "kms_glue" {
  value = aws_kms_key.glue_cmk
}
