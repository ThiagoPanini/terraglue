/* --------------------------------------------------
FILE: main.tf @ kms module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é consolidar a criação
de uma chave KMS gerenciada pelo usuário (CMK) usada
para criptografia dos insumos do job Glue, incluindo
tanto a escrita de arquivos temporários e dados no s3,
quando também a escrita de logs no cloudwatch

RESOURCES: Os recursos aqui implantados serão:
  - Chave KMS
-------------------------------------------------- */

# Criando chave KMS
resource "aws_kms_key" "glue_cmk" {
  description              = "Chave KMS utilizada para criptografia de dados escritos no S3 e logs escritos no CloudWatch"
  key_usage                = var.kms_key_usage
  customer_master_key_spec = var.kms_customer_master_key_spec
  is_enabled               = var.kms_is_enabled
  enable_key_rotation      = var.kms_enable_key_rotation
  policy                   = var.kms_policy
}

# Definindo um alias pra chave
resource "aws_kms_alias" "glue_cmk" {
  name          = "alias/kms-glue-s3"
  target_key_id = aws_kms_key.glue_cmk.key_id
}
