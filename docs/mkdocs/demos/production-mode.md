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

???+ question "Do I need to follow this exactly project structure work with terraglue?"
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
    ```json
    # Collecting data sources
    data "aws_caller_identity" "current" {}
    data "aws_region" "current" {}
    data "aws_kms_key" "glue" {
      key_id = "alias/kms-glue"
    }
    ```

And now we are ready to call the **terraglue** module and start customizing it through its variables.

## Calling the terraglue Module

In order to provide a clear vision for users, this demo will be divided into multiple records in different sections. The idea is to delivery a step by step guide showing all customizations applied to terraglue module call using the following topics:

- Calling the module from GitHub
- Setting up IAM variables
- Setting up KMS variables
- Setting up S3 scripts location
- Setting up the Glue job
- Setting up job arguments

By following all demos from each topic, users will be able to fully understand terraglue and all its different ways to deploy Glue jobs.

### Calling the module from GitHub

This section is all about showing how to call the terraglue module directly from GitHub.

??? example "Calling the terraglue module directly from GitHub"
    [![A gif showing how to call the terraglue module from the GitHub](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-02-module.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-02-module.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```json
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
        As stated before along this documentation, terraglue has a lot of variables and most of them have default values. But still there are some things to configure and customize before deploying it in a target AWS account.

        And that's why we should follow the next sections to see its configurations taking place.

### Setting Up IAM Variables

So, let's start customizing terraglue by setting some IAM variables to guide how the module will handle the IAM role needed to be assumed by the Glue job.

The module has some variables to help users to set this configuration and those can be found [in this link](../variables/variables.md#iam-configuration).

For this demo, let's set the following configurations:

- Inform terraglue that we want to create an IAM role in this project
- Inform terraglue that the IAM policies that will be part of this role are located in the `policy/` folder
- Inform terraglue the name of the IAM role to be created

??? example "Setting up IAM variables on terraglue"
    [![A gif showing how to configure IAM variables on terraglue](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-03-iam.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-03-iam.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```json
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

### Setting Up KMS Variables

Well, the next step in this demo will handle KMS key configuration that affects our Glue job. In this project, we will apply the following KMS configurations on terraglue:

- Inform terraglue to now create a KMS key during project deploy (we sill use an existing key)
- Inform terraglue the ARN of the existing KMS key (collected from the `aws_kms_key` Terraform data source declared at the beginning of the project)

??? example "Setting up KMS variables on terraglue"
    [![A gif showing how to configure KMS variables on terraglue](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-04-kms.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-04-kms.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```json
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

___

???+ warning "Work in progress"
    Content will be updated here as soon as possible!