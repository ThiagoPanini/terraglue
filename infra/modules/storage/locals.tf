/* --------------------------------------------------------
ARQUIVO: locals.tf @ storage module

Arquivo responsável por declarar variáveis/valores locais
capazes de auxiliar na obtenção de informações dinâmicas
utilizadas durante a implantação do projeto, como por
exemplo, o ID da conta alvo de implantação ou o nome da
região.
-------------------------------------------------------- */

locals {
  # Extraindo ID da conta e nome da região
  account_id  = data.aws_caller_identity.current.account_id
  region_name = data.aws_region.current.name

  # Adicionando sufixo de identificação única ao dicionário de nomes de buckets
  bucket_names_map = {
    for bucket_identifier, bucket_name in var.bucket_names_map :
    bucket_identifier => (
      substr(bucket_name, length(bucket_name) - 1, 1) == "-"
      ? "${bucket_name}${local.account_id}-${local.region_name}"
      : "${bucket_name}-${local.account_id}-${local.region_name}"
    )
  }
}






