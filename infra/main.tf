/* --------------------------------------------------
FILE: main.tf @ root module

CONTEXT: Arquivo principal de construção da infra que,
através das informações contidas nos outros arquivos
.tf e nos módulos especificados em ./modules, realiza
a especificação dos elementos a serem implantados
nos providers declarados.

GOAL: 

MODULES: A organização da infra comporta os módulos:
  - ./modules/<a definir>
Especificações e detalhes sobre o conteúdo de cada
módulo poderá ser encontrado em seus respectivos
arquivos main.tf
-------------------------------------------------- */

# Definindo data sources para auxiliar na nomenclatura de variáveis
data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

# Chamando módulo storage
module "storage" {
  source = "./modules/storage"

  bucket_name            = "sbx-sor-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
  local_data_path        = var.local_data_path
  flag_upload_data_files = var.flag_upload_data_files
}
