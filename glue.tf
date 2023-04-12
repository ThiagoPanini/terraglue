/* --------------------------------------------------------
FILE: glue.tf

This is probably the main file in the whole module as it is
used to specify and declare a preconfigured Glue job to be
explored by users. This file considers the usage of all
other componentes and resources already declared in other
Terrafom files, such as IAM roles.
-------------------------------------------------------- */
/*
# Uploading the Spark application script to S3
resource "aws_s3_object" "python_scripts" {
  for_each = local.glue_files
  bucket   = var.glue_scripts_bucket_name
  key      = "${var.glue_scripts_bucket_prefix}/${each.value}"
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

# Defining a Glue job
resource "aws_glue_job" "job" {
  # Setting job attributes
  name              = var.glue_job_name
  role_arn          = aws_iam_role.glue_job_role.arn
  description       = var.glue_job_description
  glue_version      = var.glue_job_version
  max_retries       = var.glue_job_max_retries
  timeout           = var.glue_job_timeout
  worker_type       = var.glue_job_worker_type
  number_of_workers = var.glue_job_number_of_workers

  # Setting script location and python version
  command {
    script_location = "s3://${var.glue_scripts_bucket_name}/${var.glue_scripts_bucket_prefix}/app/src/${var.glue_script_file_name}"
    python_version  = var.glue_job_python_version
  }
}

*/
