/* --------------------------------------------------------
FILE: versions.tf @ root module

This file sets up details for Terraform and its required
providers version to be used on deploying the infrastructure.
-------------------------------------------------------- */

terraform {
  required_version = ">=1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.61"
    }
  }
}
