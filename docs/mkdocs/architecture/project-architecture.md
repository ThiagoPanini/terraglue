# Project Architecture

## Infrastructure Provided

Now that *terraglue* was introduced with all its features and a [simple tutorial page](../quickstart/basic-tutorial.md) showing how to activate all of that, it's time to bring more technical aspects into the game.

At the end of the day, *terraglue* is a IaC (Infrastructure as Code) project built with [Terraform](https://www.terraform.io/) runtime and splited into modules. Each module holds resources from differente AWS services.

[![A diagram with user perspective](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/diagram-user-view.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/diagram-user-view.png)

In essence, all terraform modules declared on *terraglue* are used to define the following AWS resources:

- 🪣 S3 buckets for storing data and *assets*
- 🚨 IAM policies and role for managing access
- 🎲 Databases and tables in the Data Catalog
- ✨ A Glue job with an end to end ETL example developed using pyspark

Once deployed, *terraglue* will offer their users all services defined on the following diagram:

[![A diagram with AWS services deployed](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/diagram-product-view.png)](https://raw.githubusercontent.com/ThiagoPanini/terraglue/feature/terraglue-refactor/docs/assets/imgs/architecture/diagram-product-view.png)


## Repository Structure

Considering the project architecture presented above, the table below shows how the structure of source repository.

| 📂 **Folder** | ⚙️ **Desceiption** |
| :-- | :-- |
| `./app` | Here you can find an example of a Python script that holds a Spark application to be deployed as a Glue job on AWS. The application considers the creation of a [SoT](https://www.linkedin.com/pulse/difference-between-system-record-source-truth-santosh-kudva/) (*Source of Truth*) table using a public dataset |
| `./data` | In this directory, users will be able to identify all data sources available provided as default for improving analytics skills using AWS services. The files are presented in a special way in order to simulate a standard Data Lake structure (e.g. `db/table/file.ext`). |
| `./docs` | In this directory, users will be able to find all the diagrams and images used in the project documentation. |
| `./infra` | In this directory, users will find all Terraform declared infrastructure. The root module is divided into submodules, each one responsible for defining AWS services to be deploys as part of *terraglue* features. |