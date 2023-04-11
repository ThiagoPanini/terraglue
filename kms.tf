/* --------------------------------------------------------
FILE: kms.tf

This file is used to declare a KMS key with a custom policy
to be used in the Glue job security configuration
-------------------------------------------------------- */

# Creating a KMS key
resource "aws_kms_key" "glue_cmk" {
  count                    = var.flag_create_kms_key ? 1 : 0
  description              = "KMS Key for encrypting S3 data and CloudWatch logs"
  key_usage                = "ENCRYPT_DECRYPT"
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  is_enabled               = true
  enable_key_rotation      = false
}

# Defining a key alias
resource "aws_kms_alias" "glue_cmk" {
  count         = var.flag_create_kms_key ? 1 : 0
  name          = "alias/kms-glue-s3"
  target_key_id = aws_kms_key.glue_cmk[count.index].key_id

  depends_on = [
    aws_kms_key.glue_cmk
  ]
}
