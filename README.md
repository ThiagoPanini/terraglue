<div align="center">
    <br><img src="https://github.com/ThiagoPanini/terraglue/blob/main/docs/assets/imgs/header-readme.png?raw=true" alt="terraglue-logo">
</div>

<div align="center">
  <br>
  
  ![GitHub release (latest by date)](https://img.shields.io/github/v/release/ThiagoPanini/terraglue?color=purple)
  ![GitHub Last Commit](https://img.shields.io/github/last-commit/ThiagoPanini/terraglue?color=purple)
  ![CI workflow](https://img.shields.io/github/actions/workflow/status/ThiagoPanini/terraglue/ci-main.yml?label=ci)
  [![Documentation Status](https://readthedocs.org/projects/terraglue/badge/?version=latest)](https://terraglue.readthedocs.io/pt/latest/?badge=latest)

</div>

## Table of Contents
- [Table of Contents](#table-of-contents)
- [What is terraglue?](#what-is-terraglue)
- [Features](#features)
- [How Does it Work?](#how-does-it-work)
- [Combining Solutions](#combining-solutions)
- [Read the Docs](#read-the-docs)
- [Contacts](#contacts)
- [References](#references)

___

## What is terraglue?

Hi everyone! Welcome to the official documentation page for **terraglue**, an open source Terraform module developed in order to provide an easy way to deploy a Glue job in any AWS account.

- Are you using Glue for the first time and want to see an end to end ETL example in AWS?
- Do you already have a Spark application and want to deploy it as a Glue job in AWS?
- Do you want to automate the Glue job setup using an IaC tool such as Terraform?
- Have you ever wanted to go the next level on developing Glue jobs?

> **Note**
>  Now the *terraglue* project has an official documentation in readthedocs! Visit the [following link](https://terraglue.readthedocs.io/en/latest/) and check out usability technical details, practical examples and more!


## Features

- ✌️ Available in two different operation modes: "learning" and "production"
- 🤖 Possibility to deploy a preconfigured Glue job with a complete end-to-end ETL example when using "learning" mode
- 🚀 Possibility to deploy a custom Glue job according to user needs when using "production" mode
- 👉 Have your Glue job ready and running at the touch of a Terraform module call

___

## How Does it Work?

When users want to call **terraglue** module from the GitHub source, an operation mode must be chosen. According to this decision, different things happens in the target AWS account.

???+ info "🤖 Learning mode"
    The learning mode helps users to understand more about Glue jobs on AWS by providing a complete example with all resources needed to start exploring Glue. It works as following:

    1. A pyspark application is uploaded in a given S3 bucket to be the main script for the Glue job
    2. An auxiliar python file is also uploaded in S3 with useful transformation functions for the job
    3. An IAM role is created with basic permissions to run a Glue job
    4. A KMS key is created to be used in the job security configuration
    5. Finally, a preconfigured Glue job is deployed in order to provide users a example of a SoT table creation using Brazilian E-Commerce data from [datadelivery](https://datadelivery.readthedocs.io/en/latest/)

???+ info "🚀 Production mode"
    The production mode enables users to configure and deploy their own Glue jobs in AWS. Its operation depends on how users configure variables on module call. In summary, it works as following:

    1. In this mode, users have the chance to use all the terraglue module variables to customize the deploy
    2. A custom Glue job is deployed in the target AWS account using the variables passed by users on module call

## Combining Solutions

The *terraglue* Terraform module isn't alone. There are other complementary open source solutions that can be put together to enable the full power of learning analytics on AWS. [Check it out](https://github.com/ThiagoPanini) if you think they could be useful for you!

![A diagram showing how its possible to use other solutions such as datadelivery, terraglue and sparksnake](https://github.com/ThiagoPanini/datadelivery/blob/main/docs/assets/imgs/products-overview-v2.png?raw=true)

## Read the Docs

- Work in progress

## Contacts

- :fontawesome-brands-github: [@ThiagoPanini](https://github.com/ThiagoPanini)
- :fontawesome-brands-linkedin: [Thiago Panini](https://www.linkedin.com/in/thiago-panini/)
- :fontawesome-brands-hashnode: [panini-tech-lab](https://panini.hashnode.dev/)

___

## References

**_AWS Glue_**
- [AWS - Glue Official Page](https://aws.amazon.com/glue/)
- [AWS - Jobs Parameters Used by AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-etl-glue-arguments.html)
- [AWS - GlueContext Class](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-glue-context.html#aws-glue-api-crawler-pyspark-extensions-glue-context-create_dynamic_frame_from_catalog)
- [AWS - DynamicFrame Class](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-pyspark-extensions-dynamic-frame.html)
- [Stack Overflow - Job Failing by Job Bookmark Issue - Empty DataFrame](https://stackoverflow.com/questions/50992655/etl-job-failing-with-pyspark-sql-utils-analysisexception-in-aws-glue)
- [AWS - Calling AWS Glue APIs in Python](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-calling.html)
- [AWS - Using Python Libraries with AWS Glue](https://docs.aws.amazon.com/glue/latest/dg/aws-glue-programming-python-libraries.html#aws-glue-programming-python-libraries-zipping)
- [Spark Temporary Tables in Glue Jobs](https://stackoverflow.com/questions/53718221/aws-glue-data-catalog-temporary-tables-and-apache-spark-createorreplacetempview)
- [Medium - Understanding All AWS Glue Import Statements and Why We Need Them](https://aws.plainenglish.io/understanding-all-aws-glue-import-statements-and-why-we-need-them-59279c402224)
- [AWS - Develop and test AWS Glue jobs Locally using Docker](https://aws.amazon.com/blogs/big-data/develop-and-test-aws-glue-version-3-0-jobs-locally-using-a-docker-container/)
- [AWS - Creating OpenID Connect (OIDC) identity providers](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html)

**_Terraform_**
- [Terraform - Hashicorp Terraform](https://www.terraform.io/)
- [Terraform - Conditional Expressions](https://developer.hashicorp.com/terraform/language/expressions/conditionals)
- [Stack Overflow - combine "count" and "for_each" on Terraform](https://stackoverflow.com/questions/68911814/combine-count-and-for-each-is-not-possible)

**_Apache Spark_**
- [SparkByExamples - Pyspark Date Functions](https://sparkbyexamples.com/pyspark/pyspark-sql-date-and-timestamp-functions/)
- [Spark - Configuration Properties](https://spark.apache.org/docs/latest/configuration.html)
- [Stack Overflow - repartition() vs coalesce()](https://stackoverflow.com/questions/31610971/spark-repartition-vs-coalesce)
  
**_GitHub_**
- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/#summary)
- [Semantic Release](https://semver.org/)
- [GitHub - Angular Commit Message Format](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#-commit-message-format)
- [GitHub - commitlint](https://github.com/conventional-changelog/commitlint)
- [shields.io](https://shields.io/)
- [Codecoverage - docs](https://docs.codecov.com/docs)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Continuous Integration with GitHub Actions](https://endjin.com/blog/2022/09/continuous-integration-with-github-actions)
- [GitHub - About security hardening with OpenID Connect](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)
- [GitHub - Securing deployments to AWS from GitHub Actions with OpenID Connect](https://www.eliasbrange.dev/posts/secure-aws-deploys-from-github-actions-with-oidc/#:~:text=To%20be%20able%20to%20authenticate,Provider%20type%2C%20select%20OpenID%20Connect.)
- [GitHub - Workflow syntax for GitHub Actions](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Eduardo Mendes - Live de Python #170 - GitHub Actions](https://www.youtube.com/watch?v=L1f6N6NcgPw&t=3043s&ab_channel=EduardoMendes)

**_Docker_**
- [GitHub Docker Run Action](https://github.com/marketplace/actions/docker-run-action)
- [Using Docker Run inside of GitHub Actions](https://aschmelyun.com/blog/using-docker-run-inside-of-github-actions/)
- [Stack Overflow - Unable to find region when running docker locally](https://stackoverflow.com/questions/62546743/running-aws-glue-jobs-in-docker-container-outputs-com-amazonaws-sdkclientexcep)

**_Testes_**
- [Eduardo Mendes - Live de Python #167 - Pytest: Uma Introdução](https://www.youtube.com/watch?v=MjQCvJmc31A&)
- [Eduardo Mendes - Live de Python #168 - Pytest Fixtures](https://www.youtube.com/watch?v=sidi9Z_IkLU&t)
- [Databricks - Data + AI Summit 2022 - Learn to Efficiently Test ETL Pipelines](https://www.youtube.com/watch?v=uzVewG8M6r0&t=1127s)
- [Real Python - Getting Started with Testing in Python](https://realpython.com/python-testing/)
- [Inspired Python - Five Advanced Pytest Fixture Patterns](https://www.inspiredpython.com/article/five-advanced-pytest-fixture-patterns)
- [getmoto/moto - mock inputs](https://github.com/getmoto/moto/blob/master/tests/test_glue/fixtures/datacatalog.py)
- [Codecov - Do test files belong in code coverage calculations?](https://about.codecov.io/blog/should-i-include-test-files-in-code-coverage-calculations/)
- [Jenkins Issue: Endpoint does not contain a valid host name](https://issues.jenkins.io/browse/JENKINS-63177)

**_Outros_**
- [Differences between System of Record and Source of Truth](https://www.linkedin.com/pulse/difference-between-system-record-source-truth-santosh-kudva/)
- [Olist Brazilian E-Commerce Data](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [Stack Overflow - @staticmethod](https://stackoverflow.com/questions/6843549/are-there-any-benefits-from-using-a-staticmethod)

