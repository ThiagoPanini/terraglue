/* --------------------------------------------------
FILE: main.tf @ glue module

CONTEXT: Arquivo principal para declaração de recursos
relacionados ao tema analytics dentro dos objetivos do
projeto Terraform.

GOAL: Consolidar a criação de um job do glue com todas
as configurações necessárias de acordo com as melhroes
práticas de implementação deste serviço.

RESOURCES: Os recursos aqui implantados serão:
  - Objetos no S3 com insumos do job
  - Glue Job
  - Trigger para Glue Job
-------------------------------------------------- */

# Realizando o upload da aplicação Spark para o S3
resource "aws_s3_object" "glue_app" {
  for_each = fileset(var.glue_app_src_dir, "**.py")
  bucket   = var.glue_job_bucket_name
  key      = "jobs/${var.glue_job_name}/src/${each.value}"
  source   = "${var.glue_app_src_dir}/${each.value}"
}

# Definindo recurso para criação de security configuration
resource "aws_glue_security_configuration" "glue_sc" {
  name = "${var.glue_job_name}-security-config"

  encryption_configuration {
    cloudwatch_encryption {
      cloudwatch_encryption_mode = var.glue_cloudwatch_encryption_mode
      kms_key_arn                = var.glue_kms_key_arn
    }

    job_bookmarks_encryption {
      job_bookmarks_encryption_mode = var.glue_job_bookmark_encryption_mode
    }

    s3_encryption {
      s3_encryption_mode = var.glue_s3_encryption_mode
      kms_key_arn        = var.glue_kms_key_arn
    }

  }
}

# Declarando job do glue
resource "aws_glue_job" "this" {
  name              = var.glue_job_name
  role_arn          = var.glue_job_role_arn
  description       = var.glue_job_description
  glue_version      = var.glue_job_version
  max_retries       = var.glue_job_max_retries
  timeout           = var.glue_job_timeout
  worker_type       = var.glue_job_worker_type
  number_of_workers = var.glue_job_number_of_workers

  command {
    script_location = "s3://${var.glue_job_bucket_name}/jobs/${var.glue_job_name}/src/${var.glue_script_file_name}"
    python_version  = var.glue_job_python_version
  }

  execution_property {
    max_concurrent_runs = var.glue_job_max_concurrent_runs
  }

  default_arguments = var.glue_job_default_arguments

  security_configuration = var.glue_apply_security_configuration ? aws_glue_security_configuration.glue_sc.name : ""
}

# Declarando trigger para agendamento de job glue
resource "aws_glue_trigger" "job_trigger" {
  name     = "trigger-${var.glue_job_name}"
  type     = "SCHEDULED"
  schedule = var.glue_job_trigger_cron_expr

  actions {
    job_name = var.glue_job_name
  }
}
