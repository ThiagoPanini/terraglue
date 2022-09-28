/* --------------------------------------------------
FILE: provider.tf @ root module

CONTEXT: Arquivo de configuração do provider a ser
utilizado no módulo root desta especificação da infra.

GOAL: O objetivo deste arquivo é especificar o
provedor AWS como principal fonte de implantação dos
recursos definidos no arquivo main.tf, além de 
consolidar a autenticação necessária para a implantação
dos recursos em uma conta AWS definida pelas chaves
de acesso fornecidas e referenciadas como variáveis
no arquivo variables.tf
-------------------------------------------------- */

# Configurando provider da AWS
provider "aws" {
  shared_config_files      = var.aws_provider_config["config"]
  shared_credentials_files = var.aws_provider_config["credentials"]
}
