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
- [Contacts](#contacts)
- [References](#references)

___

## What is terraglue?

The *terraglue* project was created for helping people to improve their learning journey on AWS Glue service. It accomplishes that by enabling a pocket environment with all necessary componentes to start developing jobs, including S3 buckets, sample data on Data Catalog, IAM roles and policies, a pre configured Athena workgroup and finally an end to end Glue job example that reads, transform and catalog new data.

- Have you ever wanted to learn Glue but you stuck on a complex environment set up?
- Have you ever wanted to test an idea for an ETL in a pocket and disposable environment?
- Have you ever wanted to go the next level on developing Glue jobs?

:waning_gibbous_moon: Try *terraglue*!

> **Note**
>  Now the *terraglue* project has an official documentation in readthedocs! Visit the [following link](https://terraglue.readthedocs.io/en/latest/) and check out usability technical details, practical examples and more!


## Features

- 🚀 Have a pocket and disposable AWS environment with all infrastructure needed to start developing Glue jobs
- 🤖 No need to to worry about bucket creation, IAM roles and policies definition or even uploading datasets in your AWS account
- 📊 Possibility to run queries on different public datasets written and catalogged for users to improve their analytics skills
- 🛠️ Usage of Terraform as IaC tool for providing a consistent infrastructure
- 🔦 Turn in and turn off whenever wanted to

___

## Contacts

- [Thiago Panini - LinkedIn](https://www.linkedin.com/in/thiago-panini/)
- [paninitechlab @ hashnode](https://panini.hashnode.dev/)

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

