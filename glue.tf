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
