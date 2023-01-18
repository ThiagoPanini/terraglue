/* --------------------------------------------------
FILE: variables.tf @ kms module

CONTEXT: Arquivo de declaração de variáveis a ser 
utilizado nos recursos criados especificamente neste
módulo.

GOAL: O objetivo deste arquivo é concentrar a declaração
de variáveis para a criação de chave KMS gerenciada
pelo usuário (CMK)
-------------------------------------------------- */

variable "kms_key_usage" {
  description = "Específica a intenção de uso da chave"
  type        = string
}

variable "kms_customer_master_key_spec" {
  description = "Específica se a chave KMS contém uma chave simétrica ou assimétrica"
  type        = string
}

variable "kms_is_enabled" {
  description = "Flag para indicar se a chave está habilitada"
  type        = bool
}

variable "kms_enable_key_rotation" {
  description = "Flag para habilitar a rotação da chave"
  type        = bool
}

variable "kms_policy" {
  description = "Arquivo de policy para gerenciar acessos da chave KMS"
  type        = string
}
