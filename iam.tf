/* --------------------------------------------------------
FILE: iam.tf

This file handles the declaration of Terraform resources
used to create an IAM role for running a Glue job. It uses
the ./policy folder to read the JSON files to create all
policies needed for the role.
-------------------------------------------------------- */

# Defining the truste policy for Glue service
data "aws_iam_policy_document" "glue_trust" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["glue.amazonaws.com"]
    }
  }
}

# Creating role for Glue Crawler with all policies created previously
resource "aws_iam_role" "glue_job_role" {
  count = var.mode == "learning" || var.flag_create_iam_role ? 1 : 0

  name               = var.glue_role_name
  assume_role_policy = data.aws_iam_policy_document.glue_trust.json

  managed_policy_arns = [
    for p in aws_iam_policy.glue : p.arn
  ]

  depends_on = [
    aws_iam_policy.glue
  ]
}
