/* --------------------------------------------------
FILE: main.tf @ storage module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: O objetivo deste arquivo é consolidar a criação
de um bucket s3 alvo de todo o armazemaneto das fontes
de dados a serem utilizadas como origens do script
glue implantado.

RESOURCES: Os recursos aqui implantados serão:
  - Bucket S3 para dados soR
  - Bucket S3 para query results do Athena
  - Arquivos de fontes de dados com prefixos
-------------------------------------------------- */

# Definindo bucket s3
resource "aws_s3_bucket" "this" {
  for_each      = var.bucket_names_map
  bucket        = each.value
  force_destroy = true
}

# Definindo bloqueio de acesso público ao bucket
resource "aws_s3_bucket_public_access_block" "all_private" {
  for_each = var.flag_s3_block_public_access ? var.bucket_names_map : {}
  bucket   = aws_s3_bucket.this[each.key].id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Criptografando bucket
resource "aws_s3_bucket_server_side_encryption_configuration" "encryption" {
  for_each = var.bucket_names_map
  bucket   = aws_s3_bucket.this[each.key].bucket
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

# Adicionando arquivos locais como tabelas
resource "aws_s3_object" "data_sources" {
  for_each = var.flag_upload_data_files ? fileset(var.local_data_path, "**") : []
  bucket   = aws_s3_bucket.this["sor"].bucket
  key      = each.value
  source   = "${var.local_data_path}${each.value}"
  #etag                   = filemd5("${var.local_data_path}${each.value}")
  server_side_encryption = "aws:kms"
}


