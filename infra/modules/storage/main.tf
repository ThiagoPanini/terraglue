/* --------------------------------------------------------
FILE: main.tf @ storage module

Arquivo Terraform criado para gerenciar a declaração de
todos os recursos relacionados a serviços e elementos de
armazenamento do projeto datadelivery, tais quais:

- Buckets S3 para armazenamento de dados
- Arquivos de vários formatos a serem usados como datasets
-------------------------------------------------------- */

# Criando buckets S3 conforme dicionário previamente definido
resource "aws_s3_bucket" "datadelivery_buckets" {
  for_each      = local.bucket_names_map
  bucket        = each.value
  force_destroy = true
}

resource "aws_s3_bucket_public_access_block" "private_config" {
  for_each = var.flag_block_public_access_from_buckets ? local.bucket_names_map : {}
  bucket   = aws_s3_bucket.datadelivery_buckets[each.key].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Configurando criptografia padrão nos buckets
resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
  for_each = local.bucket_names_map
  bucket   = aws_s3_bucket.datadelivery_buckets[each.key].bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

# Realizando o upload de datasets públicos de exemplo
resource "aws_s3_object" "module_public_datasets" {
  for_each               = var.flag_upload_public_datasets ? fileset("${path.module}/data/", "**") : []
  bucket                 = aws_s3_bucket.datadelivery_buckets[var.raw_data_key_on_bucket_names_map].bucket
  key                    = each.value
  source                 = "${path.module}/data/${each.value}"
  server_side_encryption = "aws:kms"

  depends_on = [
    aws_s3_bucket.datadelivery_buckets
  ]
}

# Realizando o upload de datasets próprios fornecidos pelo usuário
resource "aws_s3_object" "user_custom_datasets" {
  for_each               = var.flag_upload_custom_datasets ? fileset(var.custom_dataset_dir, "**") : []
  bucket                 = aws_s3_bucket.datadelivery_buckets[var.raw_data_key_on_bucket_names_map].bucket
  key                    = each.value
  source                 = "${var.custom_dataset_dir}/${each.value}"
  server_side_encryption = "aws:kms"

  depends_on = [
    aws_s3_bucket.datadelivery_buckets
  ]
}
