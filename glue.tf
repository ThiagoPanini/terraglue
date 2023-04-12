/* --------------------------------------------------------
FILE: glue.tf

This is probably the main file in the whole module as it is
used to specify and declare a preconfigured Glue job to be
explored by users. This file considers the usage of all
other componentes and resources already declared in other
Terrafom files, such as IAM roles.
-------------------------------------------------------- */

# Uploading the Spark application script to S3
resource "aws_s3_object" "python_scripts" {
  for_each = local.glue_files
  bucket   = var.glue_scripts_s3_bucket
  key      = "${var.glue_scripts_s3_bucket_prefix}/${each.value}"
  source   = "${path.module}/${each.value}"
}

# Defining a Glue security configuration
resource "aws_glue_security_configuration" "glue_sc" {
  name = "${var.glue_job_name}-security-config"

  encryption_configuration {
    cloudwatch_encryption {
      cloudwatch_encryption_mode = var.glue_cloudwatch_encryption_mode
      kms_key_arn                = local.kms_key_arn
    }

    job_bookmarks_encryption {
      job_bookmarks_encryption_mode = var.glue_job_bookmark_encryption_mode
    }

    s3_encryption {
      s3_encryption_mode = var.glue_s3_encryption_mode
      kms_key_arn        = local.kms_key_arn
    }

  }
}

# ToDo: pensar no cenário onde usuário não quer criar
# uma chave KMS. Como fica aws_kms_key.glue_cmk[0].arn?
