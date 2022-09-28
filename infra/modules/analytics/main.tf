/* --------------------------------------------------
FILE: main.tf @ analytics module

CONTEXT: Arquivo principal de construção de parte
específica da infraestrutura cabível ao contexto do
módulo em questão.

GOAL: 

RESOURCES: Os recursos aqui implantados serão:
  - Databases no Glue Data Catalog
-------------------------------------------------- */

# Criando database no glue catalog
resource "aws_glue_catalog_database" "source" {
  for_each = toset(var.glue_databases)
  name     = each.value
}
