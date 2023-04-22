# Production Mode

So, let's take a deep dive on how an user can call the terraglue module to deploy it's own Glue job in AWS.

For this task, let's suppose we want to:

1. Deploy a Glue job using a Spark application already available
2. Create and associate an IAM role to the job
3. Use an already available KMS key from the AWS account to create a Security Configuration
4. Define some custom job arguments

## Structuring a Terraform Project

By essence, the first step to be done is to set up a Terraform project. For this task, it's important to mention that everyone is free to structure a Terraform project the best way they want. To make things as simple as possible, the Terraform project structure below considers the following:

- A `app/` folder to store the Spark application, additional python files and unit tests
- A `policy/` folder to store a JSON file that will be used to create an IAM role for the job
- A `main.tf` Terraform file to call terraglue module

Let's see it in a tree?

```bash
├───app
│   ├───src
│   │       main.py
│   │       utils.py
│   │
│   └───tests
│           test_main.py
│
├───policy
│       glue-job-policy.json
│
│   main.tf
```

??? question "Do I need to follow this exactly project structure in order to work with terraglue?"
    No, you don't and that's one of the coolest terraglue features. You can take any Terraform project in any structure and call terraglue without any worries.

    You will just need to pay attention to the module variables you pass during the call. To see a full list of all acceptable variables, check the [Variables](../variables/variables.md) section. The [Validations](../variables/validations.md) section is also a good page to read in order to be aware of some input variable conditions based on specific scenarios.

If you need more information about the structure of a Terraform project you can check the [official Hashicorp documentation](https://developer.hashicorp.com/terraform/language/modules/develop/structure) about it.

## Collecting Terraform Data Sources

Once we structured the Terraform project, let's start by collecting some [Terraform data sources](https://developer.hashicorp.com/terraform/language/data-sources) that will be used along the project. To get and use Terraform data sources can improve the development of a Terraform project in a lot of aspects. In the end, this is not a required step, but it can be considered as a good practice according to which resources will be declared and which configurations will be applied.

So, let's take our `main.tf` file and get the three Terraform data sources stated balow:

- A [aws_caller_identity](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) data source to extract the user account id
- A [aws_region](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) data source to get the target AWS region
- A [aws_kms_key](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/kms_key) data source to get a KMS key by its alias (assuming that there is a KMS key alias in the target AWS account)

??? example "Collecting Terraform data sources"
    [![A video demo showing how to get Terraform data sources](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-01-datasources.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-01-datasources.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```python
    # Collecting data sources
    data "aws_caller_identity" "current" {}
    data "aws_region" "current" {}
    data "aws_kms_key" "glue" {
      key_id = "alias/kms-glue"
    }
    ```

And now we are ready to call the **terraglue** module and start customizing it through its variables.

## Configuring Terraglue

In order to provide a clear vision for users, this demo will be divided into multiple records in different sections. The idea is to delivery a step by step guide showing all customizations applied to terraglue module call using the following topics:

- Calling the module from GitHub
- Setting up IAM variables
- Setting up KMS variables
- Setting up S3 scripts location
- Setting up the Glue job
- Setting up job arguments

By following all demos from each topic, users will be able to fully understand terraglue and all its different ways to deploy Glue jobs.

### Calling The Source Module

This section is all about showing how to call the terraglue module directly from GitHub.

??? example "Calling the terraglue module directly from GitHub"
    [![A gif showing how to call the terraglue module from the GitHub](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-02-module.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-02-module.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```python
    # Collecting data sources
    data "aws_caller_identity" "current" {}
    data "aws_region" "current" {}
    data "aws_kms_key" "glue" {
      key_id = "alias/kms-glue"
    }

    # Calling terraglue module in production mode
    module "terraglue" {
      source = "git::https://github.com/ThiagoPanini/terraglue?ref=main"
    }
    ```

    ___

    ???+ info "There are more things to setup before deploying terraglue"
        As stated before in this documentation, terraglue has a lot of variables and most of them has default values. But still there are some things to configure and customize before deploying it in a target AWS account.

        Optionally, users can initialize the terraglue module declared through `terraform init` command in order to get a simple but huge feature: the autocomplete text in variable names from the module. This can make things a lot easier whe configuring terraglue in the next sections.

        [![A demo gif showing the execution of the terraform init command](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-02b-init.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-02b-init.gif?raw=true)
 

### Setting Up IAM Variables

So, let's start customizing terraglue by setting some IAM variables to guide how the module will handle the IAM role needed to be assumed by the Glue job.

For this demo, let's set the following configurations:

- Inform terraglue that we want to create an IAM role in this project
- Inform terraglue that the IAM policies that will be part of this role are located in the `policy/` folder
- Inform terraglue the name of the IAM role to be created

??? example "Setting up IAM variables on terraglue"
    [![A gif showing how to configure IAM variables on terraglue](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-03-iam.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-03-iam.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```python
    # Collecting data sources
    data "aws_caller_identity" "current" {}
    data "aws_region" "current" {}
    data "aws_kms_key" "glue" {
      key_id = "alias/kms-glue"
    }

    # Calling terraglue module in production mode
    module "terraglue" {
      source = "git::https://github.com/ThiagoPanini/terraglue?ref=main"

      # Setting up IAM variables
      flag_create_iam_role = true
      glue_policies_path   = "policy"
      glue_role_name       = "terraglue-demo-glue-role"
    }
    ```

    :material-alert-decagram:{ .mdx-pulse .warning } To see more about all IAM configuration variables available on terraglue, [check this link](../variables/variables.md#iam-configuration).

### Setting Up KMS Variables

Well, the next step in this demo will handle KMS key configuration that affects our Glue job. In this project, we will apply the following KMS configurations on terraglue:

- Inform terraglue to now create a KMS key during project deploy (we sill use an existing key)
- Inform terraglue the ARN of the existing KMS key (collected from the `aws_kms_key` Terraform data source declared at the beginning of the project)

??? example "Setting up KMS variables on terraglue"
    [![A gif showing how to configure KMS variables on terraglue](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-04-kms.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-04-kms.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```python
    # Collecting data sources
    data "aws_caller_identity" "current" {}
    data "aws_region" "current" {}
    data "aws_kms_key" "glue" {
      key_id = "alias/kms-glue"
    }

    # Calling terraglue module in production mode
    module "terraglue" {
      source = "git::https://github.com/ThiagoPanini/terraglue?ref=main"

      # Setting up IAM variables
      flag_create_iam_role = true
      glue_policies_path   = "policy"
      glue_role_name       = "terraglue-demo-glue-role"

      # Setting up KMS variables
      flag_create_kms_key = false
      kms_key_arn         = data.aws_kms_key.glue.arn
    }
    ```

    :material-alert-decagram:{ .mdx-pulse .warning } To see more about all KMS configuration variables available on terraglue, [check this link](../variables/variables.md#kms-key-configuration).

### Setting Up S3 Scripts Location

After the successfully configuration of IAM and KMS variables, it's time to set up a bucket reference which will be considered by terraglue to store all Glue scripts files in the project.

Basically, this is the step where users provide a bucket name to host the files located in the `app/` project folder in order to be used in the Glue job.

In this demo, we will use the `aws_caller_identity` and `aws_region` data sources collected at the beginning of the project to build a bucket name without hard coding informations such as account ID and AWS region.

??? example "Setting up a s3 bucket name to store scripts files"
    [![A gif showing how to configure S3 variables on terraglue](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-05-s3.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-05-s3.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```python
    # Collecting data sources
    data "aws_caller_identity" "current" {}
    data "aws_region" "current" {}
    data "aws_kms_key" "glue" {
      key_id = "alias/kms-glue"
    }

    # Calling terraglue module in production mode
    module "terraglue" {
      source = "git::https://github.com/ThiagoPanini/terraglue?ref=main"

      # Setting up IAM variables
      flag_create_iam_role = true
      glue_policies_path   = "policy"
      glue_role_name       = "terraglue-demo-glue-role"

      # Setting up KMS variables
      flag_create_kms_key = false
      kms_key_arn         = data.aws_kms_key.glue.arn

      # Setting up S3 scripts location
      glue_scripts_bucket_name = "datadelivery-glue-assets-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"
    }
    ```

    :material-alert-decagram:{ .mdx-pulse .warning } To see more about all S3 configuration variables available on terraglue, [check this link](../variables/variables.md#s3-files).

### Setting Up A Glue Job

And here we probably have the most important configuration set of a terraglue module call: the Glue job set up.

The idea with this variables block is:

- Inform terraglue to associate a name to the Glue job
- Inform terraglue to associate a description to the Glue job
- Inform terraglue to use G.1X workers
- Inform terraglue to use 5 workers

??? example "Setting up a Glue job"
    [![A gif showing how to configure Glue job variables on terraglue](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-06-gluejob.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-06-gluejob.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```python
    # Collecting data sources
    data "aws_caller_identity" "current" {}
    data "aws_region" "current" {}
    data "aws_kms_key" "glue" {
      key_id = "alias/kms-glue"
    }

    # Calling terraglue module in production mode
    module "terraglue" {
      source = "git::https://github.com/ThiagoPanini/terraglue?ref=main"

      # Setting up IAM variables
      flag_create_iam_role = true
      glue_policies_path   = "policy"
      glue_role_name       = "terraglue-demo-glue-role"

      # Setting up KMS variables
      flag_create_kms_key = false
      kms_key_arn         = data.aws_kms_key.glue.arn

      # Setting up S3 scripts location
      glue_scripts_bucket_name = "datadelivery-glue-assets-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"

      # Setting up Glue
      glue_job_name              = "terraglue-sample-job"
      glue_job_description       = "A sample job using terraglue with production mode"
      glue_job_worker_type       = "G.1X"
      glue_job_number_of_workers = 5
    }
    ```

    :material-alert-decagram:{ .mdx-pulse .warning } To see more about all Glue configuration variables available on terraglue, [check this link](../variables/variables.md#job).

### Setting Up Job Arguments

And finally, it's important to show how users can input their own Glue job arguments on terraglue. In fact, it can be done through the `glue_job_args` module variable that accepts a `map` object with all user arguments in order to customize the Glue job.

The main key points about the job arguments declared in this demo are:

- Set `--job-bookmark-option` in order to disable job bookmarks from the job
- Set `--additional-python-modules` in order to use the [sparksnake](https://sparksnake.readthedocs.io/en/latest/) Python package as an additional python module
- Set `--extra-py-files` in order to add a utils.py file uploaded in this same project as an extra Python file to be used in the job

In this step, users are free to set all Glue acceptable arguments. A full list can be found in the [AWS official documentation about job parameters](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html).

??? example "Setting up Glue job arguments"
    [![A gif showing how to configure Glue job arguments on terraglue](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-07-jobargs.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-07-jobargs.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```python
    # Collecting data sources
    data "aws_caller_identity" "current" {}
    data "aws_region" "current" {}
    data "aws_kms_key" "glue" {
      key_id = "alias/kms-glue"
    }

    # Calling terraglue module in production mode
    module "terraglue" {
      source = "git::https://github.com/ThiagoPanini/terraglue?ref=main"

      # Setting up IAM variables
      flag_create_iam_role = true
      glue_policies_path   = "policy"
      glue_role_name       = "terraglue-demo-glue-role"

      # Setting up KMS variables
      flag_create_kms_key = false
      kms_key_arn         = data.aws_kms_key.glue.arn

      # Setting up S3 scripts location
      glue_scripts_bucket_name = "datadelivery-glue-assets-${data.aws_caller_identity.current.account_id}-${data.aws_region.current.name}"

      # Setting up Glue
      glue_job_name              = "terraglue-sample-job"
      glue_job_description       = "A sample job using terraglue with production mode"
      glue_job_worker_type       = "G.1X"
      glue_job_number_of_workers = 5

      # Setting up job args
      glue_job_args = {
        "--job-language"                     = "python"
        "--job-bookmark-option"              = "job-bookmark-disable"
        "--enable-metrics"                   = true
        "--enable-continuous-cloudwatch-log" = true
        "--enable-spark-ui"                  = true
        "--encryption-type"                  = "sse-s3"
        "--enable-glue-datacatalog"          = true
        "--enable-job-insights"              = true
        "--additional-python-modules"        = "sparksnake"
        "--extra-py-files"                   = "s3://datadelivery-glue-assets-${data.aws_caller_identity.current.  account_id}-${data.aws_region.current.name}/jobs/  terraglue-sample-job/app/src/utils.py"
      }
    }
    ```

And with this subsection we reach the end of the demos related to terraglue module configuration. 

___

## Running Terraform Commands

After all this configuration journey, we now just need to plan and apply the deployment using the respective Terraform commands.

### Terraform plan

Well, now it's time to see the deployment plan using the `terraform plan` command.

Here we will be able to see all the resources that will be deployed with the configuration we chose.

??? example "Running the terraform plan command"
  [![A gif showing how to run terraform plan Terraform comand](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-08-plan.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-08-plan.gif?raw=true)

### Terraform apply

And now we can finally deploy the infrastructure declared using the `terraform apply` command.

??? example "Running the terraform apply command"
  [![A gif showing how to run terraform apply Terraform comand](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-09-apply.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-09-apply.gif?raw=true)
  

## Deployed Resources