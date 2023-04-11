/* --------------------------------------------------------
FILE: provider.tf @ root module

This file is used for setting up provider credentials in a
local environment project usage. This is a good way for
not storing credentials inside the code, but using an AWS
credentials file insetad.
-------------------------------------------------------- */

provider "aws" {
  shared_config_files      = var.aws_provider_config["config"]
  shared_credentials_files = var.aws_provider_config["credentials"]
}
