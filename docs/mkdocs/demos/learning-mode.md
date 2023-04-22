# Learning Mode

What if users don't have a custom Glue job to be deployed but still they want to see and learn more about all the pieces needed to make a Glue job run in AWS? Well, the **learning mode** on terraglue can be used to deploy a preconfigured Glue job with everything is needed to see things running in practice.

In this demo we will take the following steps:

1. Structure a simple Terraform project
2. Call [datadelivery](https://datadelivery.readthedocs.io/en/latest/) Terraform module to deploy auxiliar infrastructure in the target AWS account
3. Call terraglue on learning mode to deploy a preconfigured Glue job that uses datadelivery data to create an ETL sample process

When calling terraglue on learning mode, the following actions will be applied:

1. An IAM role will be created will basic permissions
2. A KMS key will be created in order to handle job security configuration
3. A preconfigured Glue job will be created with a Spark application that reads, transform and write E-commerce data


## Structuring a Terraform Project

As we are talking about using terraglue to deploy a preconfigured Glue job, everything can be put in a single `main.tf` Terraform file. If you checked the [production mode demo](production-mode.md) you saw that the Terraform project structured in that context was a little bit more complex.

???+ question "Why do I need only a main.tf Terraform file when using terraglue on learning mode?"
    Well, there is no need to have different folders in our project to address Glue scripts files, policies or anything. By using terraglue on learning mode, all those elements, files and folders are located inside the module (you can check it on the `.terraform/` folder after running the `terraform init` command).

If you need more information about the structure of a Terraform project you can check the [official Hashicorp documentation](https://developer.hashicorp.com/terraform/language/modules/develop/structure) about it.

## Collecting Terraform Data Sources

Once we structured the Terraform project, let's start by collecting some [Terraform data sources](https://developer.hashicorp.com/terraform/language/data-sources) that will be used along the project. Terraform data sources can improve the development of a Terraform project in a lot of aspects. In the end, this is not a required step, but it can be considered as a good practice according to which resources will be declared and which configurations will be applied.

So, let's take our `main.tf` file and get the three Terraform data sources stated balow:

- A [aws_caller_identity](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/caller_identity) data source to extract the user account id
- A [aws_region](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/data-sources/region) data source to get the target AWS region

??? example "Collecting Terraform data sources"
    [![A video demo showing how to get Terraform data sources](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-01-datasources.gif?raw=true)](https://github.com/ThiagoPanini/terraglue/blob/feature/improve-docs/docs/assets/gifs/terraglue-production-01-datasources.gif?raw=true)

    ___

    💻 **Terraform code**:
    ```python
    # Collecting data sources
    data "aws_caller_identity" "current" {}
    data "aws_region" "current" {}
    ```

Before calling terraglue module, let's call the [datadelivery](https://datadelivery.readthedocs.io/en/latest/) module in order to deploy buckets, data files, catalog tables and other useful things that is mandatory to use terraglue on learning mode!


## Configuring Datadelivery

> datadelivery is an open source Terraform module that provides an infrastructure toolkit to be deployed in any AWS account in order to help users to explore analytics services like Athena, Glue, EMR, Redshift and others. It does that by uploading and cataloging public datasets that can be used for multiple purposes, either to create jobs or just to query data using AWS services.



## Configuring Terraglue

## Running Terraform Commands

## Deployed Resources

___

???+ warning "Work in progress"
    Content will be updated here as soon as possible!