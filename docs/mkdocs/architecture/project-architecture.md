# Project Architecture

## Infrastructure Provided

Now that *terraglue* was introduced with all its features and a [simple tutorial page](../quickstart/basic-tutorial.md) showing how to activate all of that, it's time to bring more technical aspects into the game.

At the end of the day, *terraglue* is a IaC (Infrastructure as Code) project built with [Terraform](https://www.terraform.io/) runtime and splited into modules. Each module holds resources from differente AWS services.

![](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/diagram-user-view.png)

In summary, all terraform modules declared on *terraglue* are used to define the following AWS resources:

- 🪣 S3 buckets for storing data and *assets*
- 🚨 IAM policies and role for managing access
- 🎲 Databases and tables in the Data Catalog
- ✨ A Glue job with an end to end ETL example developed using pyspark

Once deployed, *terraglue* will offer their users all services defined on the following diagrams:

![](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/diagram-product-view.png)


## Repo Organization