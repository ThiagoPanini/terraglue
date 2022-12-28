/* --------------------------------------------------
FILE: main.tf @ glue module

CONTEXT: Arquivo principal para declaração de recursos
relacionados ao tema analytics dentro dos objetivos do
projeto Terraform.

GOAL: Consolidar a criação de um job do glue com todas
as configurações necessárias de acordo com as melhroes
práticas de implementação deste serviço.

RESOURCES: Os recursos aqui implantados serão:
  - Glue Job
-------------------------------------------------- */

# Realizando o upload da aplicação Spark para o S3
resource "aws_s3_object" "glue_app" {
  for_each = fileset(var.glue_app_src_dir, "**.py")
  bucket   = var.glue_job_bucket_name
  key      = "jobs/${var.glue_job_name}/src/${each.value}"
  source   = "${var.glue_app_src_dir}/${each.value}"
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
}
