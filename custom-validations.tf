/* --------------------------------------------------------
FILE: custom-validations.tf @ root module

This is a special file. According to discussions in the
issue #25609 of the source Terraform project (the official
one), Terraform can't handle variables validation using
a condition that references other variable but the one which
is been validated.

It means that if users want to apply a validate condition
in a Terraform variable (e.g. "x") that uses information about
another Terraform variable (e.g. "y"), the error below is
thrown:

The condition for variable "x" can only refer to the variable
itself, using var.y.

So, according to https://github.com/hashicorp/terraform/issues/25609,
@gdsotirov provided a temporary solution that uses the
output clause with its new precondition block (since 
Terraform v1.2.0) to apply custom condition checks in
Terraform variables.
-------------------------------------------------------- */

# Validate if users provided an IAM role ARN in case of flag_create_iam_role is false
output "validate_glue_role_arn" {
  value = null

  precondition {
    condition     = (var.flag_create_iam_role == false && var.glue_role_arn != "")
    error_message = "The module was configured to not create an IAM role (var.flag_create_iam_role = false) but it wasn't passed any IAM role ARN to be assumed by the Glue job."
  }
}
