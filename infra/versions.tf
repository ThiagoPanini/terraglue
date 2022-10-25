/* --------------------------------------------------
FILE: versions.tf @ root module

CONTEXT: Arquivo de configuração do Terraform e dos
provedores requeridos para a implantação da infra
definida no projeto.

GOAL: O objetivo deste arquivo é centralizar as
dependências de versões do próprio terraform e também
dos providers envolvidos no projeto. Considerando
este projeto, define-se, neste arquivo, a utilização
do provider aws em versões próximas à 4.20.
-------------------------------------------------- */

terraform {
  required_version = ">=1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.20"
    }
  }
}
