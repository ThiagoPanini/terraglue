/* --------------------------------------------------------
FILE: locals.tf

This file handles declaration of locals variables that can
be used along other Terraform files to help users to
organize elements and componentes for all resources to be
deployed in this infrastructure project
-------------------------------------------------------- */

# Defining data sources to help local variables
data "aws_caller_identity" "current" {}
data "aws_region" "current" {}

# Defining local variables to be used on the module
locals {
  # Referencing a policies folder where the JSON files for policies are located
  iam_policies_path = "${path.module}/policy/"
}
