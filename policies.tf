/* --------------------------------------------------------
FILE: policies.tf

This is file specially created to handle the creation of
all policies needed for the project in a single Terraform
block. The idea is to loop over all JSON files in ./policy
project folder and create an individual IAM policy for each
file.

Then, the policies can be used in other Terraform file of
this module, such as iam.tf and kms.tf.
-------------------------------------------------------- */

# Creating IAM policies to be used in a IAM role for a Glue job
resource "aws_iam_policy" "glue" {
  for_each = fileset(local.glue_policies_path, "**")
  name     = split(".", each.value)[0]
  policy   = file("${local.glue_policies_path}/${each.value}")
}
