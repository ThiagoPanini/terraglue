# Variables Validations

When building a Terraform module, it's really important to be aware of restrictions relatead to user inputs. For things work properly, some module variables need to be passed in a certain way and following some rules. That's why this documenation page exists: to explain all input variables validations included on terraglue.

??? tip "The different ways that variables were validated in terraglue"
    If you are familiar with Terraform code, you know that it's possible to validate a variable input using the [validation](https://developer.hashicorp.com/terraform/language/values/variables#custom-validation-rules) block code when declaring a variable. In fact, this is a really straitghforward way to apply custom rules in order to validate any variable input. The example below shows how to use the `validation` block code to apply a variable validation based on a condition.

    ```python
    variable "image_id" {
      type        = string
      description = "The id of the machine image (AMI) to use for the server."

      validation {
          condition     = length(var.image_id) > 4 && substr(var.image_id, 0, 4) == "ami-"
          error_message = "The image_id value must be a valid AMI id, starting with \"ami-\"."
      }
    }
    ```

    But there is a crucial limitation when using the validation block code for this task: it only allows to use the variable that is beeing validated on the rules. In other words, if we want to validate the user input in one variable based on a condition that needs to check another variable, an error is thrown.

    ???+ warning "The Terraform #25609 issue"
        So, According to discussions in the issue #25609 of the source Terraform project (the official one), Terraform can't handle variables validation using a condition that references multiple variables.

        It means that if users want to apply a validate condition in a variable (e.g. "x") using information about another variable (e.g. "y"), the error below is thrown:

        ```The condition for variable "x" can only refer to the variable itself, using var.y.```

    In order to workaround this limitation, the solution provided by user [@joeaawad](https://github.com/joeaawad) in [this topic](https://github.com/hashicorp/terraform/issues/25609#issuecomment-1057614400) shows that it's possible to use the `locals.tf` Terraform file to apply variables validation using conditions based on multiple variables. In the example below two variables are declared and a `locals` block is used in order to apply a custom variable validation with a condition that uses both variables:

    ```python
    variable "versioning" {
      default = true
    }

    variable "lifecycle_rules" {
      default = null
    }

    locals {
      # tflint-ignore: terraform_unused_declarations
      validate_versioning = (var.versioning && var.lifecycle_rules == null) ? tobool("Please pass in lifecycle_rules or change versioning to false.") : true
    }
    ```

    Now that we know more about the main way to validate Terraform variables and a workaround that fits well to validations that needs to use a condition based in multiple variables, it's important to state some points about how those topics are related to terraglue:

    :material-alert-decagram:{ .mdx-pulse .warning } Terraglue applies both ways explained above in different situations along the project. Some variables are validated using the classic way. But there are some variables that need to be validated based on the value of other variables, so the `locals` approach is necessary.

In this documenation page, users will be able to see all validations applied on terraglue module variables. The idea is to provide a full comprehension about how things works and to delivery more power to users in order to call terraglue in the right way.

## Operation Mode

In this subsection we will see all validations applied to terraglue operation mode.

??? warning "Validating the `var.mode` variable"
    The first validation on terraglue is applied on `var.mode` variable in order to make sure users are selecting only operation modes that are available. Let's see how this variable is declared.

    ```python
    variable "mode" {
      description = "Defines an operation mode that enables users to choose to use the module for learning or production/development purposes"
      type        = string
      default     = "production"

      validation {
        condition     = contains(["learning", "production"], var.mode)
        error_message = "Acceptable values for mode variable are: 'learning', 'production'"
      }
    }
    ```

    So, this leads to a variable validation that forces users to pass the values `"learning"` or `"production"` to `var.mode` variable.

## KMS Configuration

Let's see all the validations applied on variables that help users to configure KMS key actions on terraglue.

??? warning "Validating `var.kms_key_alias` variable"
    The `var.kmd_key_alias` is used to reference an existing KMS key alias on the target AWS account to be used in encryption steps when creating a Glue job. Let's see how this variable is declared:

    ```python
    variable "kms_key_alias" {
      description = "Alias for the KMS key created. Users should pass this variable in case of var.flag_create_kms_key is true"
      type        = string
      default     = "alias/kms-glue-s3"

      validation {
        condition     = substr(var.kms_key_alias, 0, 6) == "alias/"
        error_message = "Variable kms_key_alias must start with 'alias/' prefix. Example: alias/kms-glue-s3"
      }
    }
    ```

    Well, by looking at the `condition` block, it's possible to say that this validation ensures that users pass an alias that starts with `"alias/"` prefix. The KMS key alias is used to collect the `aws_kms_key` Terraform data source by alias and if users don't inform a valid alias, an error is thrown.

## Glue Setup

Terraglue provides to users different ways to customize their Glue jobs to be deployed in AWS. Uncle ben once said that "with great power comes great responsibility" and so, validations needed to be applied to Glue jobs variables configuration on terraglue. Let's see them all.

??? warning "Validating `var.glue_scripts_bucket_prefix` variable"
    The `var.glue_scripts_bucket_prefix` variable enables the possibility to choose a bucket prefix to store all the Glue files related to the job that is beeing deployed. By default, it has the `"jobs/"` value but users can choose a different prefix. Let's see how this variable is declared:

    ```python
    variable "glue_scripts_bucket_prefix" {
      description = "An optional S3 prefix to organize Glue application files"
      type        = string
      default     = "jobs/"

      validation {
        condition     = var.glue_scripts_bucket_prefix == "" || substr(var.glue_scripts_bucket_prefix, -1, -1) == "/"
        error_message = "The application dir value has special characteres. Only a-z, A-Z and 0-9 characteres are allowed."
      }
    }
    ```

    Well, the condition block shows two things:
    - The variable can't assume an empty value (e.g. "")
    - The variable must end with "/"

    This is important because strings concatenation during the execution of terraglue in order do create S3 reference variables (such as S3 URI that uses bucket name, prefix, and file names).


## Production Mode Validations

??? warning "Validations applied on terraglue's production mode"
    Different validations are applied to terraglue if users choose to call it on production mode. They are all shown below:

    ```python
    # Validating ARNs for IAM role and KMS key
    validate_glue_role_arn = (var.mode != "learning" && var.flag_create_iam_role == false && var.glue_role_arn == "") ? tobool("The module was configured to not create an IAM role (var.flag_create_iam_role = false) but it wasn't passed any IAM role ARN to be assumed by the Glue job.") : true
    validate_kms_key_arn   = (var.mode != "learning" && var.flag_create_kms_key == false && var.kms_key_arn == "") ? tobool("The module was configured to not create a KMS key (var.flag_create_kms_key = false) but it wasn't passed any KMS key ARN to be used in Glue job encryption tasks.") : true
    ```

    Both validations shown above are related to the same situation and it takes place when the following scenario is true:

    - Users choose to call terraglue on production mode (`var.mode != "learning"`)
    - Users don't want to create an IAM role or a KMS key (`var.flag_create_iam_role == false`) 
    - Users don't pass an ARN for IAM role or KMS key to be used on the job (`var.glue_role_arn == ""`)

    Well, if users are telling terraglue that they want to deploy their own Glue jobs (production mode) and they don't want to create an IAM role or neither a KMS key, they must pass a valid ARN for the role or either for the key.

    A Glue job can't be deployed without those infos. So either users provide the ARNs or configure terraglue to let it create those elements.

## Learning Mode validations

??? warning "Validations applied on terraglue's learning mode"
    The same way as it has variables validations when users call terraglue on production mode, there are also specific conditions that are applied when they call it on learning mode.

    Let's see them all:

    ```python
    # Validating output bucket and database variables when learning mode is called
    validate_output_bucket_name = (var.mode == "learning" && var.job_output_bucket_name == "") ? tobool("When calling the module with learning mode, it's necessary to provide a valid bucket name for the job_output_bucket_name variable") : true
    validate_output_database    = (var.mode == "learning" && var.job_output_database == "") ? tobool("When calling the module with learning mode, it's necessary to provide a database name for the job_output_db variable") : true
    ```

    So, the things is:

    - When using learning mode, users must inform two variables:
      - `job_output_bucket_name`
      - `job_output_database`
    
    That's why the terraglue learning mode has a preconfigured Glue job that reads, transform and write data. So, the job needs to be informed about the output elements to be used when writing data to s3 (`job_output_bucket_name`) and cataloging it on Data Catalog (`job_output_database`).

That's all about variables validations. If you are still in trouble when trying to use terraglue, please feel free to open [an issue](https://github.com/ThiagoPanini/terraglue/issues/new/choose) on the source repository.