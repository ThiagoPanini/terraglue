/* --------------------------------------------------
FILE: outputs.tf @ iam module

CONTEXT: Arquivo de definição de outputs a serem usados
em arquivos externos à este módulo.

GOAL: O objetivo deste arquivo é permitir que outros
recursos definidos neste projeto possam utilizar 
policies e roles IAM aqui descritas.
-------------------------------------------------- */

output "lambda-basic-role" {
  description = "Role iam com permissões básicas de log para funções lambda"
  value       = aws_iam_role.lambda-basic-role.arn
}

output "lambda-103" {
  description = "Role iam com permissões de coleta de arquivo csv de bucket s3"
  value       = aws_iam_role.lambda-103.arn
}

output "lambda-104" {
  description = "Role iam com permissões de coleta de arquivo csv de bucket s3"
  value       = aws_iam_role.lambda-104.arn
}

output "lambda-105" {
  description = "Role iam com permissões para ligar e desligar instancias ec2"
  value       = aws_iam_role.lambda-105.arn
}

output "lambda-106" {
  description = "Role iam com permissões de deletar volumes ebs em uma conta aws"
  value       = aws_iam_role.lambda-106.arn
}

output "lambda-107" {
  description = "Role iam com permissões de coleta de arquivo csv de bucket s3"
  value       = aws_iam_role.lambda-103.arn
}

output "lambda-108" {
  description = "Role iam com permissões de coleta de arquivo csv de bucket s3"
  value       = aws_iam_role.lambda-103.arn
}
