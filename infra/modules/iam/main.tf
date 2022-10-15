/* --------------------------------------------------
FILE: main.tf @ iam module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é centralizar a criação
de policies e roles do IAM a serem utilizadas pelos
demais recursos e serviços deste projeto de infra

RESOURCES: Os recursos aqui implantados serão:
  - IAM Policies
  - IAM Roles
-------------------------------------------------- */

# Definindo data sources para auxiliar na nomenclatura de variáveis
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "glue_trust" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}



