/* --------------------------------------------------------
FILE: variables.tf @ storage module

Arquivo de variáveis criado para alimentar o submódulo de
storage dentro do projeto datadelivery
-------------------------------------------------------- */

variable "glue_scripts_dir_path" {
  description = "Referência de diretório no projeto onde encontra-se os arquivos a serem armazenados no S3 para serem utilizados no job Glue."
  type        = string
}
